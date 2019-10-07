import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask_wtf import CSRFProtect
from flask_restful import Api
from flask_migrate import Migrate

app=Flask(__name__)


BASE_DIR=os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR=os.path.join(BASE_DIR,'static')

app.secret_key ='123456'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR,'ORM.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

models=SQLAlchemy(app)
# csrf=CSRFProtect(app)
api=Api(app)
migrate=Migrate(app,models)