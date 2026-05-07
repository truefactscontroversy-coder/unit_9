from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import os
import secrets
from flask import session

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
    admin_key = db.Column(db.String(100), unique=True)

    def __init__(self, admin_key):
        self.admin_key = admin_key

class admin_keySchema(ma.Schema):
    admin_key = fields.Str()

admin_key_schema = admin_keySchema()
admin_key_schemas = admin_keySchema(many=True)



@app.route('/get_all_weather_data', methods=['GET'])
def get_weather_data():
    all_weather_data = weather_data.query.all()
    result = weather_data_schemas.dump(all_weather_data)
    return jsonify(result)


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