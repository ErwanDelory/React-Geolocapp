""" Flask File """
from flask import Flask
from flask_cors import CORS
from Controllers.controller import controller

app = Flask(__name__)
CORS(app)
app.register_blueprint(controller, url_prefix="/api")

@app.route('/', methods=['GET'])
def home():
    """ Default Route """
    return "<h1>Home</h1><p>This is the home page</p>"

if __name__ == "__main__":
    app.run(debug=True)
