from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class weather_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(100), unique=True)
    date = db.Column(db.String(100))
    am1 = db.Column(db.Float)
    am2 = db.Column(db.Float)
    pm1 = db.Column(db.Float)
    pm2 = db.Column(db.Float)

    def __init__(self, area, date, am1, am2, pm1, pm2):
        self.area = area 
        self.date = date
        self.am1 = am1
        self.am2 = am2
        self.pm1 = pm1
        self.pm2 = pm2


class weather_dataSchema(ma.Schema):
    area = fields.Str()
    date = fields.Str()
    am1 = fields.Float()
    am2 = fields.Float()   
    pm1 = fields.Float()
    pm2 = fields.Float()



weather_data_schema = weather_dataSchema()
weather_data_schemas = weather_dataSchema(many=True)




if __name__ == '__main__':
    app.run(debug=True)