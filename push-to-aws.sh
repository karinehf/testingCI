source AWS-env-var.sh
cd app
pip install awscli
eval $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION) #needs AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
export AWS_ACCOUNT_ID="$( aws sts get-caller-identity --output text --query Account )"
docker build -t $AWS_IMAGE_NAME:latest .
docker tag $AWS_IMAGE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$AWS_REPO
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$AWS_REPO:latest

#Using Fargate or dynamic port mapping + load balancer
#aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --force-new-deployment