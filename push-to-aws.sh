cd app
AWS_REPO=app-image-repo
AWS_CLUSTER=app-image-cluster
AWS_SERVICE=app_image_service
AWS_IMAGE_NAME=app_image_test
AWS_DEFAULT_REGION=eu-west-1

pip install awscli
export PATH=$PATH:$HOME/.local/bin
eval $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION) #needs AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
docker build -t $AWS_IMAGE_NAME:latest .
docker tag $AWS_IMAGE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$AWS_REPO
#docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$AWS_REPO:latest
#aws ecs update-service --cluster $AWS_CLUSTER --service $AWS_SERVICE --force-new-deployment


#Keep a copy, so we can alter the above
# - cd app
# - pip install awscli
# - export PATH=$PATH:$HOME/.local/bin
# - eval $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION) #needs AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
# - docker build -t app_image:latest .
# - docker tag app_image:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/app-image-repo
# - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/app-image-repo:latest
# - aws ecs update-service --cluster api-image-cluster --service api_image_service --force-new-deployment