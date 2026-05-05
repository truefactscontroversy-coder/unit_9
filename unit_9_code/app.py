from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class weather_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    districts = db.Column(db.String(100), unique=True)
    am_1read = db.Column(db.Float)
    am_2read = db.Column(db.Float)
    pm_1read = db.Column(db.Float)
    pm_2read = db.Column(db.Float)

    def __init__(self, districts, am_1read, am_2read, pm_1read, pm_2read):
        self.districts = districts
        self.am_1read = am_1read
        self.am_2read = am_2read
        self.pm_1read = pm_1read
        self.pm_2read = pm_2read

class username(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

class weather_dataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'districts', 'am_1read', 'am_2read', 'pm_1read', 'pm_2read')

class usernameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

weather_data_schema = weather_dataSchema(strict=True)
weather_data_schemas = weather_dataSchema(many=True, strict=True)
username_schema = usernameSchema(strict=True)



if __name__ == '__main__':
    app.run(debug=True)