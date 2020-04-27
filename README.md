# Using Travis CI (testingCI repository)
This repository shows how to connect a GitHub Repo and AWS ECR using Travis CI. 
Travis tests running a Flask application using Docker service and runs other tests defined by user.
Then, if all tests are passed, Travis pushes a Docker image to AWS ECR.
Currently working with Flask app, Docker, Travis CI and AWS ECR.

# Key points
## Keep as in this repository
- Repository structure
- Health endpoint in `app/app.py`
- `app/docker-compose.yml` except the container port
- Names of environmental variables in `AWS-env-var.sh`

## Change/add to your repository
- Connect your github repository to Travis CI
- Update root directory name and variable `app_name` in `app/app.py`
- Add app content and update requirements for the app and `app/Dockerfile` settings
- Set ports in `app/Dockerfile` or `app/app.py` and `app/docker-compose.yml`
- Add/change content of `tests/test_content.py`
- Store AWS non-secret variables in `AWS-env-var.sh`
- Store AWS keys in an encrypted way using correct naming

# Connect your GitHub repo to Travis CI
To connect Travis CI to your repository, do steps 1-3 in <https://docs.travis-ci.com/user/tutorial/#to-get-started-with-travis-ci-using-github>. The file `.travis.yml` tells Travis what to do when a build is triggered (that is, when you push something to the master branch of your repository).

## .travis.yml
This file should be in your root folder for Travis to find it. Most commands are written elsewhere, as we want to keep this file clean.
Travis-specific settings can, however, be changed here if necessary: 
- Set another version of Python
- Make pushes to other branch than Master trigger a Travis build
- Other Travis-specific restrictions or services are required for your application. More info here: <https://docs.travis-ci.com/?utm_source=help-page&utm_medium=travisweb>. 
Otherwise, functionality should be kept out of this file. The commands Travis run are in the scripts `run-docker-and-tests.sh` and `push-to-aws.sh`. Never store secrets or display/echo password in these scripts.
 
## Storing secrets
Secrets/keys etc should never be stored in plain text. They can, however, be stored encrypted in `.travis.yml` using `travis encrypt`, or as environment variables in your TravisCI settings for your repository.
1. The simplest way of saving secret keys and variables, such as your AWS keys, is as environment variables in your Travis repository settings. These are encrypted as default as long as you do *not choose to display value in build log*. See details in <https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings>. Saving your secrets in this way makes it easy to keep track of which secrets you have, and it keeps the code clean.
2. You can also add an encrypted version of your secrets to `.travis.yml`, but to keep your code clean, be careful with this. 
    First, you must install the `travis` tool, which is written in Ruby and published as a `gem`. Therefore, you need Ruby and RubyGems installed first. 
    
    **NOTE**: There might be several options here, and it might be preinstalled. As a Mac used, there was some trouble with having to use `sudo`. 
    
    Then to install `travis` and encrypt your keys, follow the procedure here: <https://docs.travis-ci.com/user/encryption-keys/#usage>. Since we are using the `.com`-site, use the `--pro` version of the commands. 
    Add your variables to `.travis.yml` together with any other variables like this:
    ```yaml
    env:
        global:
            - secure: "...encrypted string..."
            - NOT_SECRET_VARIABLE = "my_variable"
    ```
The most important secrets in this repository are the AWS access keys. Some additional information about these is provided in section [Push docker image to AWS](#Push-docker-image-to-AWS).

# Repository details
**NOTE**: In general, your repo should include the folders and files and the same structure as this template repository for all Travis commands and tests to run without error. 

Folder names `app` and `tests` must be kept as they are, as must name of app content file: `app.py`. Root directory should be the name of the app, and the variable `app_name` must also be added as a variable in `app.py`.
The YAML file `.travis.yml` must be in root directory, and so should the `.sh`-scripts be. These are called from `.travis.yml` and include the specific commands Travis needs to run.
The `.vscode` folder with settings include some settings convenient for running the unit tests in Visual Studio Code. Here, it is specified where to look for the tests and to use Python 3 by default. The folder is not necessary for running the tests in Travis or from other interfaces.
The `.gitignore` file is a genereric gitignore for python projects, and can be customized. 
The requirements-file inside `app` should include everything needed for the app, and the `requirements.txt` in root directory must include what Travis needs. What is needed to run the unit tests is included here, and the app's requirements should also be referred to: 

```python
-r app/requirements.txt
```
For the content of `app` and `tests` folders, see the following sections.

## Running and testing application
The `app` folder is where you add your app functionality. Update your app content and Docker settings inn `app/app.py` and `app/Dockerfile`, as well as the requirements for the app in `app/requirements.txt`. Add the health endpoint as structured in `app.py`. 
The file `app/docker-compose.yml` is only used to run tests. The name of the service in this file must be 'app'. Port mapping must be added to run the app, and for the tests to run, the container port must also be updated in `docker-compose.yml`.
This is how and where you set your container port: 
- If using gunicorn in `Dockerfile`, there are two alternatives: 
    1. Set container port in `Dockerfile`, and set the same container port in `docker-compose.yml`.  
    2. Only set the container port in `docker-compose.yml` to 8000, which is gunicorn default.
- If gunicorn is not used, there are also two alternatives: 
    1. Set a port in `app.py` (preferably using `port` variable as in the template here) and set same container port in `docker-compose.yml`. 
    2. Only set the container port in `docker-compose.yml` to 5000, which is flask default.

**NOTE**: The functionality of the health endpoint is currently very limited.

**NOTE**: Be aware that changed settings for docker image here will be tested, but *not* included when pushing to AWS. If it is desired to use the docker-compose file to push to AWS, the docker build command in the script `push-to-aws.sh` must be changed. 

## Running tests

In the `tests` folder, all test logic is found. The test framework `unittest` is used. See <https://docs.python.org/3/library/unittest.html> for documentation. The tests are structured into three classes based on what they are testing, and these are divided into three modules: `test_content.py`, `test_structure.py` and `test_running.py`. In addition there is a `test_base.py` module, which does not contain any tests, but provides a class with functionality methods for `test_structure.py` and `test_running.py`. The methods in `test_base.py` are mainly for reading files and finding the specified ports.
All tests can be found as methods with names starting with `test_`. The tests in `test_running.py` and `test_structure.py` should work if the naming and repository structure is as in this repository. Feel free to add more tests. The most important test now, it to check that the app is responding when Travis is running the docker container. 
Content in `test_content.py` is specific for the app content. Tests for app content logic can be added here, or else just remove the template test. Content and structure tests should pass as long as code and logic is correct, while `test_running.py` needs a running container to pass, as the tests here checks for status code of a runing flask app.
Travis runs the tests by first building and running the docker image as specified in `app/docker-compose.yml`, and then the tests are run using commands on the form 

```python
python -m unittest tests/test_structure.py
```
Remember that the container port must be added in `app/docker-compose.yml` and that the service name in this file must be 'app' for Travis to run the container.

**NOTE**: Python3 is required for the imports in the tests to be valid.

**NOTE**: The tests always assume host '0.0.0.0'. If another host should be used for the tests, this must now be set in `test_running.py`. In `test_base.py` there is some starting code for extracting the host from `app/Dockerfile` or `app/app.py`, so that it does not have to be set manually for the tests, but it is not finished.

**NOTE**: Can we find a way to test i.e. container port mapping against AWS?

# Push docker image to AWS
If the tests are all passed, Travis moved to the `deploy` phase, and the docker image is pushed to AWS ECR. 
In the deployment, the docker image is built without using `app/docker-compose.yml`. 

Again, **NOTE**: Be aware that changed settings for docker image in `app/docker-compose.yml` will be tested, but *not* included when pushing to AWS. If it is desired to use the docker-compose file to push to AWS, the docker build command in the script `push-to-aws.sh` must be changed.

The commands for pushing to AWS ECR are in `push-to-aws.sh`. If you are using Fargate (or dynamic port mapping) and want to *force new deployment* when pushing a new image, uncomment the last line in this script. Otherwise, it should not be necessary to change anything in this file. The information needed to find and push to you ECR, is provided as environment variables, and you must create these The non-secret variables can be saved in the script `AWS-env-var.txt`, while secrets should be saved encrypted as described in section [Storing secrets](#storing-secrets). Be aware that to login to ECR using the command `aws ecr get-login`, the AWS access keys must be stored in (secure) variables with correct names names. The names must be `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_ACCOUNT_ID`. Never store these in plain text. You can choose which encryption method to use, but to keep `.travis.yml` clean and for you to have the best overview over your keys, saving environment variables in your Travis settings is the best option.

A suggestion for which variables you can save unencrypted is currently in `AWS-env-var.txt`, but you can choose to delete these and save them encrypted if preferred. Use the same names for the variables as in this template. You can see how the variables are used in `push-to-aws.sh`. Remember to never store keys and passwords in this script. Further, if there exists a naming convention for your container/ECR/service/cluster etc, you can add rules for this by using and editing the block commented out in `AWS-env-var.txt`. 

**NOTE**: Save these naming rules in this template if the same rules are used accross all repos/apis, so that you don't need to set all names manually. 





