from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS # frontend will need this

# from config import DATABASE_CONNECTION_URI
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
CORS(app)

db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
