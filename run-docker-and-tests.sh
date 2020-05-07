#Get container port
PORT=$(python get_port.py)

#Docker
#Build image and run container
cd app

docker build -t app_image:test .
docker run -d -p $PORT:$PORT --name app_container app_image:test

docker ps
cd -

#Run tests involving content of code:
python -m unittest tests/test_structure.py
python -m unittest tests/test_content.py 

#Tests involving the running of web app
python -m unittest tests/test_running.py

#Stop and remove the running container
cd app
docker ps
docker stop $(docker ps -q -f "name=app_container")
docker ps
docker container rm $(docker ps -a -q -f "name=app_container")
cd -

########
#Simple python script can be run like this: 
#python firsttest.py
#Running all tests in a package: 
#python -m unittest discover tests 
########

