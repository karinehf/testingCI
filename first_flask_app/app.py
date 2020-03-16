from flask import Flask
#from flask_restful import Recource, Api

app = Flask(__name__)
#api = Api(app)

@app.route("/")
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

