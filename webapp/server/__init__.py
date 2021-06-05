# This file tells python that server is a package
# NOTE: to generate the SQLite file. Need to:
# $ cd webapp
# $ py
# >>> from server import db
# >>> from server.models import Sensor, Measurement
# >>> db.create_all()
# site.db should now exist in webapp/server
#
# NOTE: db.drop_all() will clear all tables.
# (need db.create_all() to start again)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #/// => relative path from current file
db = SQLAlchemy(app)

# must import this last because routes imports app
# i.e. "from server import app" is in routes so it needs to exist before importing
from server import routes