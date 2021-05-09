from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

from backend import routes