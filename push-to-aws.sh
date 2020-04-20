cd app
pip install awscli
export PATH=$PATH:$HOME/.local/bin
aws configure list
eval $(aws ecr get-login --no-include-email --region eu-west-1) #needs AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
docker build -t app_image:latest .
docker tag app_image:latest $AWS_ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/app-image-repo
docker push $AWS_ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/app-image-repo:latest