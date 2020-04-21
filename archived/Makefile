CLUSTER_NAME = API-cluster
ACCOUNT_ID = $(shell aws sts get-caller-identity --output text --query Account)

aws_container_name = $(shell basename $(CURDIR))
# credentials from aws profile
AWS_ACCESS_KEY_ID = $(shell aws configure \
 get aws_access_key_id)
AWS_SECRET_ACCESS_KEY = $(shell aws configure \
 get aws_secret_access_key)
AWS_DEFAULT_REGION = $(shell aws configure \
 get region)

build:
	docker build -t $(aws_container_name):latest .

#aws_creds_old:
#    $(shell aws ecr get-login --no-include-email --region $(AWS_DEFAULT_REGION))    

aws_creds:
	$(shell aws ecr get-login-password | docker login --username AWS --password-stdin https://$(ACCOUNT_ID).dkr.ecr.$(AWS_DEFAULT_REGION).amazonaws.com)

aws_creds_test:
	$$(aws ecr get-login-password | docker login  --password-stdin --username AWS "459994320734.dkr.ecr.eu-west-1.amazonaws.com")




create_repo:
	aws ecr create-repository --repository-name $(aws_container_name) --region $(AWS_DEFAULT_REGION)

aws_tag:
	docker tag $(aws_container_name) $(ACCOUNT_ID).dkr.ecr.$(AWS_DEFAULT_REGION).amazonaws.com/$(aws_container_name)

ecr_push:
	docker push $(ACCOUNT_ID).dkr.ecr.$(AWS_DEFAULT_REGION).amazonaws.com/$(aws_container_name):latest
	
aws_push: build aws_creds aws_tag ecr_push

aws_redeploy_service:
	aws ecs update-service --cluster $(CLUSTER_NAME) --service $(aws_container_name)-service --force-new-deployment

aws: aws_creds build aws_tag aws_push aws_redeploy_service