#Get container port
PORT=$(python get_port.py)
#Build image and run container
cd app
docker build -t app_image:test .
docker run -d -p $PORT:$PORT --name app_container app_image:test
cd -