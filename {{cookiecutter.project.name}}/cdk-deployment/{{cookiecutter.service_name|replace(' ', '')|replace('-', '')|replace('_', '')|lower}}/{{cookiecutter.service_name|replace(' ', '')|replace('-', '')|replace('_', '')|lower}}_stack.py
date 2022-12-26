from typing import Tuple
import os

from aws_cdk import (
    Stack,
    aws_ecr as ecr, aws_ecs as ecs, aws_ec2 as ec2, aws_elasticloadbalancingv2 as elb,
    aws_iam as iam,
    aws_elasticache as cache, aws_secretsmanager as sm,
    aws_logs as logs,
    aws_ecr_assets as ecr_assets, aws_route53_targets as targets,
    RemovalPolicy, Duration, Tags, CfnOutput, 
    aws_route53 as dns
)
from constructs import Construct


service_name = "{{cookiecutter.project.slug|replace(' ', '')|replace('-', '')|replace('_', '')|lower}}-{{cookiecutter.service_name|replace(' ', '')|replace('-', '')|replace('_', '')|lower}}"
if os.path.isfile("../keys/private_key.pem"):
    with open("../keys/private_key.pem", "r+", encoding="utf-8") as file:
        rsa_private_key = file.read()
else:
    rsa_private_key = os.getenv("RSA_PRIVATE_KEY")


class {{cookiecutter.service_name|replace(' ', '')|replace('-', '')|replace('_', '')|capitalize}}Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Initial Set up
        vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=os.getenv("VPC_ID"))

        {% if cookiecutter.deployment.cdk.cluster.available == "True" %}
        # ECS Cluster
        cluster = ecs.Cluster.from_cluster_attributes(
            self, "ecs-cluster", cluster_name=os.getenv("CLUSTER_NAME"), vpc=vpc, security_groups=[])
        {% else %}
        # ECS Cluster
        cluster = ecs.Cluster(self, "ecs-cluster", cluster_name=f"{service_name}-cluster",
                              container_insights=True, vpc=vpc)
        cluster.apply_removal_policy(RemovalPolicy.DESTROY)
        {% endif %}

        # IAM Role
        ecs_role = iam.Role(
            self, "ecs-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self, "ecs-service-policy",
                    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"),
                iam.ManagedPolicy.from_managed_policy_arn(
                    self, "autoscaling-policy",
                    "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"),
                {% if cookiecutter.configuration.xray.enabled == "True" %}
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSXRayFullAccess"),
                {% endif %}
            ], role_name = f"{service_name}-ecs-role",
        )

        # Load balancer
        alb, alb_sg, target_group = self.set_up_load_balancing(vpc)

        {% if cookiecutter.caching.enabled == "True" %}
        # Redis
        redis_cluster = self.set_up_redis(vpc=vpc)  # type: ignore
        {% endif %}

        # ECS Tasks
        backend_task = self.set_up_task(ecs_role=ecs_role, task_type="backend", {% if cookiecutter.caching.enabled == "True" %}redis=redis_cluster{% endif %})

        # ECS Services
        backend_service = self.set_up_service(
            vpc=vpc, service_type="backend", alb_sg=alb_sg, cluster=cluster, task=backend_task
        )
        backend_service.attach_to_application_target_group(
            target_group=target_group)
        self.add_tags()
        self.outputs(alb=alb)

    def set_up_load_balancing(
            self, vpc: ec2.IVpc
    ) -> Tuple[elb.ApplicationLoadBalancer, ec2.SecurityGroup, elb.ApplicationTargetGroup]:
        alb_sg = ec2.SecurityGroup(self, id='alb-sg', allow_all_outbound=True, vpc=vpc)
        alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(),
                                ec2.Port.tcp(80), "Public HTTP Traffic")
        alb = elb.ApplicationLoadBalancer(
            self, 'alb', vpc=vpc, internet_facing=True,
            ip_address_type=elb.IpAddressType.IPV4)
        alb.add_security_group(alb_sg)
        target_group = elb.ApplicationTargetGroup(
            self, id="alb-target-group",
            deregistration_delay=Duration.seconds(30),
            port=8000, vpc=vpc, protocol=elb.ApplicationProtocol.HTTP, target_type=elb.TargetType.IP
        )
        target_group.configure_health_check(
            path='/healthcheck/', healthy_threshold_count=2, unhealthy_threshold_count=5,
            enabled=True, interval=Duration.seconds(20), timeout=Duration.seconds(10), protocol=elb.Protocol.HTTP)
        listener = alb.add_listener('alb-http-listener', open=True, port=80)
        listener.add_target_groups("alb-listener-target-group", target_groups=[target_group])

        # Uncomment this if you have a domain name and a certificate you want to tie to your ALB
        # domain_name = os.getenv("DOMAIN_NAME")
        # certificate_arn = os.getenv("ACM_CERTIFICATE_ARN")
        # listener.add_action(
        #     id='redirect-to-https', action=elb.ListenerAction.redirect(protocol='HTTPS', port='443'))
        # certificate = acm.Certificate.from_certificate_arn(
        #    self, certificate_arn=certificate_arn, id="ssl-certificate")
        # https_listener = alb.add_listener(
        #     'alb-https-listener', open=True, port=443, protocol=elb.ApplicationProtocol.HTTPS,
        #     certificates=[certificate])
        # https_listener.add_target_groups(
        #     "alb_listener-https-target", target_groups=[target_group])
        # self.set_up_domain(alb, domain_name)

        return alb, alb_sg, target_group

    def outputs(self, alb: elb.ApplicationLoadBalancer):
        CfnOutput(self, 'loadBalancer',
            value=alb.load_balancer_dns_name,
            description='Load balancer DNS',
            export_name=f'{service_name}-lb'
        )

    def set_up_domain(self, alb: elb.ApplicationLoadBalancer, domain_name: str):

        zone = dns.HostedZone.from_lookup(
            self, "hosted_zone", domain_name=domain_name)
        dns.ARecord(
            self, "DNS Record", record_name=service_name,
            zone=zone, target=dns.RecordTarget.from_alias(
                targets.LoadBalancerTarget(alb)
            )
        )

    def set_up_task(
            self, ecs_role: iam.IRole, task_type: str,
            {%- if cookiecutter.caching.enabled == "True" %}
            redis: cache.CfnCacheCluster,
            {% endif %}
    ) -> ecs.TaskDefinition:
        task_def = ecs.TaskDefinition(
            self, id=f"{task_type}-task-def", cpu="1024", memory_mib="4096",
            family=f"{service_name}-{task_type}-task-def", network_mode=ecs.NetworkMode.AWS_VPC,
            compatibility=ecs.Compatibility.FARGATE,
            task_role=ecs_role, execution_role=ecs_role
        )

        base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
        task_def.add_container(
            f"ecs-{task_type}-container", container_name=f"{service_name}-{task_type}-container",
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=f"{service_name}-{task_type}-logs",
                log_group=logs.LogGroup(
                    self, f"ecs-{task_type}-log-group",
                    log_group_name=f"{service_name}-{task_type}-log-group",
                    retention=logs.RetentionDays.ONE_WEEK,
                    removal_policy=RemovalPolicy.DESTROY
                )
            ),
            image=ecs.ContainerImage.from_docker_image_asset(
                  asset=ecr_assets.DockerImageAsset(
                      self,
                      id=f'{task_type}-image', directory=base_dir, exclude=[os.path.join(base_dir, 'cdk-deployment')])
            ),
            environment={
                "STAGE": "PROD",
                "TYPE": task_type.upper(),
                "RSA_PRIVATE_KEY": rsa_private_key,
                {% if cookiecutter.caching.enabled == "True" %}
                "REDIS_URL": f"redis://{redis.attr_redis_endpoint_address}:{redis.attr_redis_endpoint_port}/",
                {% endif %}
                {% if cookiecutter.configuration.xray.enabled == "True" %}
                "XRAY_DAEMON": "localhost:2000",
                "AWS_XRAY_TRACING_NAME": f"{task_type}-service",
                "AWS_XRAY_SDK_ENABLED": "true",
                {% endif %}
            },
            port_mappings = [
                              ecs.PortMapping(
                                  container_port=8000, host_port=8000, protocol=ecs.Protocol.TCP
                              ),
                            ],
            essential = True,
            entry_point = ["/bin/bash", "scripts/entrypoint.sh"]
        )
        {% if cookiecutter.configuration.xray.enabled == "True" %}
        task_def.add_container(
            "xray-daemon", container_name=f"xray-{task_type}-daemon-container",
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix=f"{service_name}-{task_type}-xray-daemon-logs",
                log_group=logs.LogGroup(
                    self, f"ecs-xray-{task_type}-daemon-log-group",
                    log_group_name=f"{service_name}-{task_type}-xray-daemon-logs-group",
                    retention=logs.RetentionDays.ONE_WEEK,
                    removal_policy=RemovalPolicy.DESTROY
                )
            ),
            image=ecs.ContainerImage.from_registry("amazon/aws-xray-daemon"),
            port_mappings=[
                ecs.PortMapping(
                    container_port=2000, host_port=2000, protocol=ecs.Protocol.TCP
                ),
                ecs.PortMapping(
                    container_port=2000, host_port=2000, protocol=ecs.Protocol.UDP
                ),
            ],
            essential=False
        )
        {% endif %}
        return task_def

    def set_up_service(
            self, vpc: ec2.IVpc, cluster: ecs.Cluster,
            alb_sg: ec2.SecurityGroup, task: ecs.TaskDefinition, service_type: str, desired_count: int = 1,
    ) -> ecs.FargateService:
        ecs_sg = ec2.SecurityGroup(
            self, f'{service_type}-ecs-sg', vpc=vpc, allow_all_outbound=True
        )
        ecs_sg.connections.allow_from(alb_sg, ec2.Port.all_tcp(), 'Application load balancer')
        ecs_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(8000))
        service = ecs.FargateService(
            self, id=f'{service_type}-service', task_definition=task,
            service_name=f'{service_name}-{service_type}-service', desired_count=desired_count,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets), cluster=cluster, security_groups=[ecs_sg],
            max_healthy_percent=200, min_healthy_percent=50
        )
        service.apply_removal_policy(RemovalPolicy.DESTROY)
        scaling = service.auto_scale_task_count(
            max_capacity=10, min_capacity=1)
        scaling.scale_on_cpu_utilization(
            f"{service_type}-cpuscaling", target_utilization_percent=60)
        return service

    {% if cookiecutter.caching.enabled == "True" %}
    def set_up_redis(self, vpc: ec2.Vpc) -> cache.CfnCacheCluster:
        subnet_ids = list(map(lambda x: x.subnet_id, vpc.private_subnets))
        cache_sg = ec2.SecurityGroup(
            self, id="cache-security-group", allow_all_outbound=True,
            vpc=vpc)
        cache_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            6379), "Redis Security group")

        cache_subnet_group = cache.CfnSubnetGroup(
            self, "redis-subnet-group",
            description="Subnet group for redis celery broker", subnet_ids=subnet_ids)
        cache_cluster = cache.CfnCacheCluster(
            self, "redis-cluster", cache_node_type="cache.t3.small", engine="redis", num_cache_nodes=1,
            cache_subnet_group_name=cache_subnet_group.cache_subnet_group_name,
            vpc_security_group_ids=[cache_sg.security_group_id])
        return cache_cluster
    {% endif %}

    def add_tags(self):
        tags = {
            "AD": "{{cookiecutter.user.ad_username}}",
            "Project": "{{cookiecutter.project.name}}",
            "Email": "{{cookiecutter.user.email}}",
            "Quarter": "TU 2022",
            "Owner": "{{cookiecutter.user.first_name}}",
            "Deletion-advice": "Do not delete"
        }
        for key, value in tags.items():
            Tags.of(self).add(key, value)