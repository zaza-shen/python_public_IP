from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.users import User
from flask_app.models.shows import Show
from flask_app.controllers import shows_control
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

#Redirect to Index need session being clear
@app.route("/session_clear")
def index_bef():
    session.clear()
    return redirect('/')

#Index
@app.route("/")
def index():
    return render_template("index.html")

#dashboard
@app.route("/shows")
def go_dashboard():
    if not session:
        return render_template('alert.html')
    data = {'id' : session['id']}
    user = User.get_one(data)
    print('--------------------', user['id'])
    return render_template("dashboard.html",user=user, allShows = Show.get_all_shows(data))
    

#Create User or Login
@app.route("/index_process", methods = ["POST"])
def register_and_login_process():
    if request.form["formName"] == "regis_form":
        data = {
            "first_name" : request.form["first_name"], 
            "last_name" : request.form["last_name"], 
            "email" : request.form["email"],
            "password" : request.form["password"],
            "c_password" : request.form["c_password"]
        }
        if not User.validate_register(data):
            return redirect("/")
        data['password'] = bcrypt.generate_password_hash(data['password'])
        temp_id = User.save(data)
        session['id'] = temp_id
        return redirect("/shows")
    elif request.form["formName"] == "login_form":
        data = {
            "email" : request.form["email"],
            "password" : request.form["password"]
        }
        # if not User.validate_email(data):
        #     return redirect('/')
        # user_pwd_in_db = User.get_pwd_by_email(data['email'])
        # # print('this is pwd_db______________', user_pwd_in_db)
        # if not bcrypt.check_password_hash(user_pwd_in_db['password'], data['password']):
        #     flash(u'Your pwd is wrong.', 'login')
        #     return redirect('/')
        # session['id'] = User.validate_email(data)['id']
        # return redirect("/shows")
        return render_template('alert.html')

#TO Unlike
@app.route('/unlike/<int:user_id>/<int:show_id>')
def to_unlike(user_id, show_id):
    # print('-----------This is unlike')
    data = {
        'user_id' : user_id,
        'show_id' : show_id
    }
    User.unlike(data)
    return redirect('/shows')

#TO Like
@app.route('/like/<int:user_id>/<int:show_id>')
def to_like(user_id, show_id):
    # print('-----------This is like')
    data = {
        'user_id' : user_id,
        'show_id' : show_id
    }
    User.like(data)
    return redirect('/shows')
