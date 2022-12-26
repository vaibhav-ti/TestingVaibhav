# CDK Deployment

## CDK Install (Optional)
If you're trying to run deployments manually on your local machine, you need to first install the aws-cdk npm package

```bash 
npm install -g aws-cdk
```

## Bootstrap CDK
CDK needs to be bootstrapped before a CDK stack can be deployed. You can check whether your current account and region is bootstrapped by going to the cloudformation console and checking for CDKToolkit stack. If the stack exists, CDK has already been bootstrapped. If not, you need the owner of the account or someone with admin permissions to bootstrap it by following these commands 

```bash
cd cdk-deployment
cdk bootstrap
```

## AWS Credentials
* For deployment using ECS CDK, you will need to create AWS Credentials for your account. The credentials must have the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudformation:DescribeStacks",
                "cloudformation:CreateChangeSet",
                "cloudformation:DescribeChangeSet",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:GetTemplate"
            ],
        "Resource": "arn:aws:cloudformation:*:<ACCOUNT_NUMBER>:stack/CDKToolkit/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:*"
            ],
            "Resource": "arn:aws:secretsmanager:*:<ACCOUNT_NUMBER>:secret:<PROJECT_SLUG>-*"
        }
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::*:role/cdk-*"
            ]
        }
    ]
}
```

`These permissions are required to bootstrap CDK, set up secrets and deploy CDK stacks respectively`

## Database Credentials
If you opted into creating a DB using the process BP platform, your service should have the DB credentials listed, in the service details, which you can copy

## VPC
Your ECS Cluster also needs a VPC ID for deployment. By defauly, the template suggest the codenationprod-main-vpc(vpc-id vpc-a533d7c2), but you can change it to whatever VPC your use case requires

NOTE: It's strongly recommended to use a VPC that is peered with central

## Environment Set up
- Copy keys from [env/.env.prod.template](env/.env.prod.template) file
- Create a `.env.prod` in the root directory and fill out the values for the environment variables.

## Run deployment through CI/CD
* Once you push the changes to the repository, the CI/CD will automatically publish the changes to ECS.

## Run deployment manually
Running deploy manually from devspaces is not possible since devspaces runs on ARM64 CPUs whereas ECS containers are currently ocnfigured for AMD64 CPUs. Hence, the docker images required for either platform are different. Trying to build cross platform docker images is error prone and we strongly recommend against it

The ideal way to do it is to let CI/CD pipelines take care of it for you, however, if you want to run things manually, we recommend using a local machine with an AMD64 CPU or legacy.devspaces.com and running the following commands
```bash
export $(cat .env.prod | xargs)
sh scripts/deploy.sh
```

## Connect a secure domain
By default, CDK deploys a load balancer, but we have also included commented code to add a secured domain to your application connected to your load balancer. Note: You need to have create verified SSL certificate for the domain if you want a secure connection 

## Remove Deployment
Run the following command
```commandline
bash scripts/destroy.sh
```

# EYK Deployment

## Download and install the EYK CLI tool for your OS:
It's recommended to do the initial set-up of EYK from your local machine

### Mac/Linux:
Open your CLI and execute the following to download and run the installation script:

```bash
$ curl -ssl https://eyk-assets.ey.io/eyk/eyk-installer.sh | bash
```

### Windows:
Use your browser to download the script, then use PowerShell to install it:
Navigate to: https://eyk-assets.ey.io/eyk/eyk-installer.ps1

[More Details](https://support.cloud.engineyard.com/hc/en-us/articles/360057913834-Download-the-Kontainers-CLI-Tool)

### Login to EYK

After the installation, open https://eyk.ey.io/app in your default browser and login to the web console.

Then, run the following in your shell. 

```bash
./eyk ssologin https://eyk.central-staging-qa.eyk-central.ey.io
```
This will log you into the central-staging-qa cluster. 

### Create an EYK App

- Using CLI
  - Run `./eyk apps:create {EYK_APP_NAME}` to create an EYK app

- Using Web Console
    - Click on the `+` icon on the top right corner of the web console
    - Select the cluster and enter the name of the app and click on `Create`

### Getting EYK HOST:

Assuming you have setup EYK cli locally on your machine,
Run following command to get command for Add EYK remote step
`git remote show eyk`
 
It would give you Push URL like this :
Push  URL: `ssh://git@eyk-builder.central-staging-qa.eyk-central.ey.io:2222/api-backend.git`

If it fails, you can get the EYK SSH host from the cluster information and then run the following commands to set the remote url.

```commandline
git remote add eyk 'ssh://git@{EYK_SSH_HOST}:2222/{EYK_APP_NAME}.git'
git push -u eyk main
```

### Getting SSH Keys:
For generating ssh keys follow [EYK docs](https://support.cloud.engineyard.com/hc/en-us/sections/360009109134-Engine-Yard-Kontainers-New-User-Guide).

If you have already setup eyk on local machine then you can use already generated private keys.

### EYK Push

```commandline
git push eyk
```

**Tips for Environment Variables:**
Use this command if you want to push all env variables stored in .env  to EYK.
```commandline
./eyk config:push
```

### Open the deployed EYK app

```commandline
./eyk open
```

### Configure Custom Domain SSL Certificate 

- Add you custom domain to the app by following the instructions from [Change DNS records](Pointing CD Pipeline Scripts to EYK)  
- Add certificate to the cluster

`./eyk certs:add <cert-name> <publickey.pem> <privkey.pem>`
    
`E.g ./eyk certs:add wildcard-eytest-link pubkey.pem privkey.pem`

- Attach the certificate to the custom domain

`./eyk certs:attach <cert-name> <custom-domain>`

`E.g. ./eyk certs:attach wildcard-eytest-link sabhttps.eytest.link`

[Full Documentation](https://docs.google.com/document/d/1oTKZriTJlJr4DpIhWxtb7JSQXQzCcFIbXY2ZIi2bsMY/)
