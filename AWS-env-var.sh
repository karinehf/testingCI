#############################
##SETTING ALL MANUALLY:
AWS_DEFAULT_REGION=eu-west-1
AWS_REPO=app-image-repo
AWS_CLUSTER=app-image-cluster
AWS_SERVICE=app_image_service
AWS_IMAGE_NAME=app_image_test

##############################
##IF THERE IS A NAMING STANDARD##
#Find app name from root directory: 
# current_dir=$PWD
# app_name="${current_dir%"${current_dir##*[!/]}"}" # extglob-free multi-trailing-/ trim
# app_name="${app_name##*/}"

#setting names based on app name and naming standard. 
# AWS_REPO=$app_name
# AWS_SERVICE=$app_name-service
# AWS_IMAGE_NAME=$app_name

# AWS_DEFAULT_REGION=eu-west-1
# AWS_CLUSTER=API-cluster
################################