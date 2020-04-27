from flask import Flask
from  healthcheck import HealthCheck #For health endpoint
import os
from flask_restplus import Resource, Api, apidoc

####################################
#Get app name from root directory:
#Works locally but not in docker
#current_dir = os.getcwd()
#root_dir = os.path.dirname(current_dir)
#app_name = os.path.basename(root_dir)
#print(app_name)
###############################

##############################
#Set name manually:
app_name = "testingCI"
#Host and port only matter if gunicorn is not used.
host = '0.0.0.0' #Currently never collected by tests.
port = None
################################

apidoc.apidoc.url_prefix = f'/{app_name}'
 
app = Flask(__name__)
api = Api(app
, title=f'{app_name}'
, doc = f'/{app_name}/'
, prefix=f'/{app_name}'
, description='My first API for testing CI, hello world and health')

health = HealthCheck(app, "/"+ app_name + "/health") #For health endpoint

@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return "Hello World!"

@api.route("/health") #For health endpoint
class HealthCheckResource(Resource):
    def get(self):
        pass

if __name__ == "__main__":
    app.run(debug = True, host = host, port = port)

