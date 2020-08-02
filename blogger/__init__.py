from flask import Flask
import os 

app = Flask(__name__)

app.secret_key = os.urandom(12)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

from blogger import models
from blogger import views