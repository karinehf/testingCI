# testingCI
This repository shows how to connect a GitHub Repo and AWS ECR using Travis CI. 
Travis tests running a Flask application using Docker service and runs other tests defined by user
Then, if all tests are passed, Travis pushes a Docker image to AWS ECR.
Currently working with Flask app, Docker, Travis CI and AWS ECR

# Summary
## Keep as is
- Repository structure
- Health endpoint in app.py
- docker-compose.yml except port


## Must change/add
- Connect github repo to Travis CI
- Root directory name and variable 'app_name' in app.py
- App content and Dockerfile settings
- Ports in Dockerfile/app.py and docker-compose.yml

# Connect your GitHub repo to Travis CI

# .travis.yml
- Most commands are moved out of .travis.yml, and this should be kept clean. 
- If a different version of python is needed, it should be changed here
- If other branches than Master should trigger a Travis build, it should be changed here
- It other Travis-specific restrictions or services are required, these can be added. 
- Otherwise, functionality should be kept out of this file. 
- Never save secrets uncrypted or display/echo passwords in this file. 
- Secrets/keys etc can be saved encrypted using travis encrypt, but can also be added as environmental variables in your TravisCI settings for your repository. 

# Repository structure
- Folder names "app" and "tests" must be kept as they are, as must name of app content: "app.py"
- Root directory should be the name of the app
- app_name must also be added as a variable in app.py
- .travis.yml must be in root directory, and so should the .sh-scripts be

# Running and testing application
- Update your app and Docker settings inn app/app.py and app/Dockerfile.
- Intend to use the health endpoint as structured in app.py. Functionality can preferably be added to this template.
- If using gunicorn in Dockerfile, set container port here, and set the same container port in docker-compose.yml, or set port in docker-compose.yml to 8000, which is gunicorn default.
- If gunicorn is not used, set a port in app.py (preferably using 'port' variable) and set same container port in docker-compose.yml. Otherwise set the port in docker-compose.yml to 5000, which is flask default.
- docker-compose.yml is only used to run tests. Therefore, be aware that changing settings for image here will be tested, but NOT included when pushing to AWS. If it is desired to use the docker-compose file for this, then the docker build command in "push-to-aws.sh" should be changed. 

# Running tests

# Push to AWS
In the deployment, the docker image is built without using docker-compose.

Add AWS variables to script. NO SECRETS.
uncomment the force-deploy command if using Fargate



