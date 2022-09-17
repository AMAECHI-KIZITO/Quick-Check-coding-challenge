from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from challenge_pkg import config
app=Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)
csrf=CSRFProtect(app)
db=SQLAlchemy(app)
from challenge_pkg.routes import view_route,api_route
from challenge_pkg import models

