export $(cat .env.prod| xargs)
cd cdk-deployment
pip install -r requirements.txt
cdk destroy --all --require-approval never