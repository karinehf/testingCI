# testingCI - Using Travis CI
This repository shows how to connect a GitHub Repo and AWS ECR using Travis CI. 
Travis tests running a Flask application using Docker service and runs other tests defined by user
Then, if all tests are passed, Travis pushes a Docker image to AWS ECR.
Currently working with Flask app, Docker, Travis CI and AWS ECR.

# Summary
## Keep as is
- Repository structure
- Health endpoint in `app.py`
- `docker-compose.yml` except container the container port

## Must change/add
- Connect github repo to Travis CI
- Root directory name and variable `app_name` in app.py
- App content, requirements for the app and `Dockerfile` settings
- Ports in `Dockerfile` or `app.py` and `docker-compose.yml`
- Content of `test_content.py`.
- AWS non-secret variables to `AWS_env_var.sh` and AWS keys in an encrypted way.

# Connect your GitHub repo to Travis CI
Do steps 1-3 here to connect Travis CI to your repository: <https://docs.travis-ci.com/user/tutorial/#to-get-started-with-travis-ci-using-github>. The file `.travis.yml` tells Travis what to do when a build is trigger (that is, when you push something to the master branch of your repository). This file should be in your root directory. See the following section about this file.

## .travis.yml
This file should be in your root folder for Travis to find it. Most commands are written elsewhere, as we want to keep this file clean.
Travis-specific settings can, however, be changed here if necessary: 
- Set another version of Python
- Make pushes to other branch than Master trigger a Travis build
- Other Travis-specific restrictions or services are required for your application. More info here: <https://docs.travis-ci.com/?utm_source=help-page&utm_medium=travisweb>. 
Otherwise, functionality should be kept out of this file. Never save secrets uncrypted or display/echo passwords in this file. 
 
## Storing secrets
Secrets/keys etc can be saved encrypted in `.travis.yml` using `travis encrypt`, or as environment variables in your TravisCI settings for your repository. For details on AWS keys, see section *Push docker image to AWS*.
1. The simplest way of saving secret keys and variables, such as your AWS keys, is as environment variables in your Travis repository settings. These are encrypted as default as long as you do not choose to *display value in build log*. See details in <https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings>.
2. You can also add an encrypted version of your secrets to `.travis.yml`, but to keep your code clean, be careful with this. 
    First, you must install the `travis tool`, which is written in Ruby and published as a gem. Therefore, you need Ruby and RubyGems installed first. **NOTE**: There might be several options here, and it might be preinstalled. As a Mac used, there was some trouble with having to use sudo. 
    Then to install `travis` and encrypt your keys, follow the procedure here: <https://docs.travis-ci.com/user/encryption-keys/#usage>. Since we are using the `.com`-site, use the `--pro` version of the commands. 
    Add your variables to `.travis.yml` together with any other variables like this:
    ```yaml
    env:
        global:
            - secure: "...encrypted string..."
            - NOT_SECRET_VARIABLE = "my_variable"
    ```


# Repository details
- **NOTE**: In general, your repo should include the folders and files and the same structure as this template repository for all Travis commands and tests to run without error. 
- Folder names `app` and `tests` must be kept as they are, as must name of app content: `app.py`
- Root directory should be the name of the app
- app_name must also be added as a variable in `app.py`
- `.travis.yml` must be in root directory, and so should the `.sh`-scripts be. These are called from `.travis.yml` and include the specific commands Travis needs to run.
- `.vscode` folder with settings include some settings convenient for running the unit tests in Visual Studio Code. It is specified where to look for the tests and to use Python 3 as default. The folder are not necessary for running the tests in Travis or from other interfaces.
- `.gitignore` file is a genereric gitignore for python projects, and can be customized. 
- The requirements-file inside `app` should include all needed for the app, and the requirements must include what Travis needs. The app's requirements should be referred to: 

```python
-r app/requirements.txt
```

In additions, what is needed to run the unit tests is included here.
- For the content of `app` and `tests` folders, see the following sections.

## Running and testing application
- Update your app and Docker settings inn `app/app.py` and `app/Dockerfile`, as well as the requirements for the app.
- Intend to use the health endpoint as structured in `app.py`. **NOTE**: The functionality of the endpoint is currently very limited.
- `docker-compose.yml` is only used to run tests. Therefore, be aware that changing settings for image here will be tested, but NOT included when pushing to AWS. **NOTE**: If it is desired to use the docker-compose file for this, then the docker build command in `push-to-aws.sh` must be changed.
- Ports must be added, and for the tests to work, the container port must be updated in `docker-compose.yml` as well. 
- If using gunicorn in `Dockerfile`, there are two alternatives: 
    1. set container port in `Dockerfile`, and set the same container port in `docker-compose.yml`.  
    2. Only set the container port in `docker-compose.yml` to 8000, which is gunicorn default.
- If gunicorn is not used, there are also two alternatives: 
    1. Set a port in `app.py` (preferably using `port` variable as in the template here) and set same container port in `docker-compose.yml`. 
    2. Only set the container port in `docker-compose.yml` to 5000, which is flask default.


## Running tests
Test running and test structure should work if the naming of the repository is used. 

docker-compose: the correct container port must be added. The service name must be `app`.

**NOTE**: The tests always assume host '0.0.0.0'. If another host should be used for the tests, this must now be set in `test_running.py`. In `test_base.py` there is some starting code for getting the host from `Dockerfile` or `app.py`, so that it does not have to be set manually for the tests, but it is not finished.

Content in `test_content`is specific for the app content. Tests for app content logic can be added here, or else just remove the template test.

The most important test is now that the docker container is running, but more tests can be added. 
**NOTE**: Can we find a way to test i.e. port mapping towards AWS?


# Push docker image to AWS
In the deployment, the docker image is built without using docker-compose.

Add AWS variables to script. NO SECRETS.
uncomment the force-deploy command if using Fargate

Make sure that the variables needed to log in to AWS are saved with the right name.



