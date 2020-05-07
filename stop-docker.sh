#Stop and remove the running container
cd app
docker ps
docker stop $(docker ps -q -f "name=app_container")
docker ps
docker container rm $(docker ps -a -q -f "name=app_container")
cd -