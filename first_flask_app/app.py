from flask import Flask, request

#from flask_restful import Recource, Api

app = Flask(__name__)
#api = Api(app)

#Not really used for anything right now..
def base_url():
    return request.base_url

@app.route("/")
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')

