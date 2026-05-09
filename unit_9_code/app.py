from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import os
import secrets
from flask import session
from sqlalchemy.orm import declarative_base, Session

app = Flask(__name__)

app.secret_key = "abc123"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class weather_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(100))
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
    class Meta:
        ordered = True
    area = fields.Str()
    date = fields.Str()
    am1 = fields.Float()
    am2 = fields.Float()   
    pm1 = fields.Float()
    pm2 = fields.Float()

weather_data_schema = weather_dataSchema()
weather_data_schemas = weather_dataSchema(many=True)
    
class user_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    api_key = db.Column(db.String(100), unique=True)

    def __init__(self, username):
        self.username = username
        self.api_key = secrets.token_urlsafe(32)


class user_infoSchema(ma.Schema):
    username = fields.Str()
    api_key = fields.Str()

username_schema = user_infoSchema()
username_schemas = user_infoSchema(many=True)

class admin_key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_for_admin = db.Column(db.String(100), unique=True)

    def __init__(self, key_for_admin):
        self.key_for_admin = key_for_admin

class admin_keySchema(ma.Schema):
    key_for_admin = fields.Str()

admin_key_schema = admin_keySchema()
admin_key_schemas = admin_keySchema(many=True)




def check_auth(func):
    def wrapper(*args,**kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            return jsonify({"error": "API key missing"}), 401
        api_keys = db.session.query(user_info.api_key).all()

        if not any(api_key in key_list for key_list in api_keys):
            return jsonify({"error": "invalid key, please enter a new key or go to the CEA website to get one"})


        return func(*args, **kwargs)
    

    wrapper.__name__ = func.__name__  
    return wrapper



@app.route('/Get_weather_data/', methods=['GET'])
@check_auth
def Get_weather_data():
    date = request.args.get('date')
    area = request.args.get('area') 

    if (date and area):
        day_data = weather_data.query.filter_by(date=date, area=area).first()
        result = weather_data_schema.dump(day_data)
        if not result:
            return jsonify({"error": "the record you tried to query does not exist"})
        else:
            return jsonify(result)
    elif (date):
        date_data = weather_data.query.filter_by(date=date).all()
        result = weather_data_schemas.dump(date_data)
        if not result:
            return jsonify({"error": "the record you tried to query does not exist"})
        else:
            return jsonify(result)
    elif (area):
        location_data = weather_data.query.filter_by(area=area).all()
        result = weather_data_schemas.dump(location_data)
        if not result:
            return jsonify({"error": "the record you tried to query does not exist"})
        else:
            return jsonify(result)
    else:
        all_weather_data = weather_data.query.all()
        result = weather_data_schemas.dump(all_weather_data)
        if not result:
            return jsonify({"error": "the record you tried to query does not exist"})
        else:
            return jsonify(result)
    


@app.errorhandler(404)
def non_existent(e):
        return jsonify({"error": "The route is miss configured or misspelled, please see the CEA website for details"})

def get_all_usernames():
    usernames_list = db.session.query(user_info.username).all()
    return usernames_list



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register.html')
def register_page():
    return render_template('register.html')

@app.route('/register_page', methods=['GET','POST'])
def register():
    username_from_form = request.form.get('username')
    username_list = get_all_usernames()
    unpack_user_list = []
    for i in username_list:
        user = list(i)
        unpack_user_list.extend(user)



    if (username_from_form not in unpack_user_list):
        db.session.add(user_info(username_from_form))
        db.session.commit()
        session["username"] = username_from_form
        return jsonify({
            "status": "success",
            "redirect": url_for("account_page")

        })
    elif not username_from_form:
        return jsonify({
            "status": "empty"
        })
    else:
         return jsonify({"status": "taken"})
         

@app.route('/usernames', methods=['GET'])
def get_usernames():
    usernames = user_info.query.all()
    result = username_schemas.dump(usernames)
    return jsonify(result)



@app.route('/user_key/', methods=['GET'])
def get_key():

    user_name = request.args.get('username')
    users_key = user_info.query.filter_by(username=user_name).first()

    if users_key is None:
        return jsonify({
            "status": "failed",
            "message": "User not found"
        }), 404

    return jsonify({
        "status": "success",
        "api_key": users_key.api_key
    })
    
@app.route('/get_admin_keys', methods=['GET'])
def get_admin_keys():
    admin_keys = admin_key.query.all()
    result = admin_key_schemas.dump(admin_keys)
    return jsonify(result)


@app.route('/account_page.html')
def account_page(): 
    username_from_session = session.get("username")
    user = user_info.query.filter_by(
        username=username_from_session
    ).first()

    return render_template(
        "account_page.html",
        username=user.username,
        api_key=user.api_key
    )

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/login_page', methods=['GET','POST'])
def login():
    username_from_form = request.form.get('username')
    username_list = get_all_usernames()
    unpack_user_list = []
    for i in username_list:
        user = list(i)
        unpack_user_list.extend(user)

    print(username_from_form)

    if (username_from_form in unpack_user_list):
         session["username"] = username_from_form
         return jsonify({
            "status": "success",
            "redirect": url_for("account_page")
        })
    else:
         return jsonify({"status": "failed"})









if __name__ == '__main__':
    app.run(debug=True)