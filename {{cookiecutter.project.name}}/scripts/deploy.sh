{% if cookiecutter.deployment.selected == 'ECS (CDK) - Recommended' %}
cd cdk-deployment
npm install -g aws-cdk
pip3 install -r requirements.txt
cdk deploy --all --require-approval never --outputs-file output.json
{% endif %}
