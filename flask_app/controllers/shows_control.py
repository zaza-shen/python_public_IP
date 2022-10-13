from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.users import User
from flask_app.models.shows import Show
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

#Show detail
@app.route("/shows/<int:r_id>")
def read_single(r_id):
    data = {'id' : session['id']}
    user = User.get_one(data)
    data = {'id' : r_id}
    poster_name = User.get_show_poster(data)
    show = Show.get_one(data)
    data = {'r_id' : r_id}
    liker_count = Show.get_liker_count(data)
    #print("This is read one_______________",single_id)
    return render_template("detail.html",user = user, show = show, poster_name = poster_name, liker_count = liker_count)


#Create Show
@app.route('/shows/new')
def newShow():
    return render_template('add.html')
@app.route("/add_process", methods=['POST'])
def addShow():
    # print(request.form["title"],'______________')
    data = {
            "title" : request.form["title"], 
            "network" : request.form["network"], 
            "descr" : request.form["descr"],
            "release_date" : request.form["release_date"],
            "user_id" : session['id']
    }
    if not Show.validate_show(data):
        return redirect('shows/new')
    Show.save(data)
    return redirect('/shows')

#edit show
@app.route('/shows/edit/<int:r_id>')
def editShow(r_id):
    return render_template('edit.html',r_id = r_id)
@app.route("/edit_process", methods=['POST'])
def editShow1():
    # print(request.form["title"],'______________')
    data = {
            'r_id' : request.form['r_id'],
            "title" : request.form["title"], 
            "network" : request.form["network"], 
            "descr" : request.form["descr"],
            "release_date" : request.form["release_date"],
            "user_id" : session['id']
    }
    if not Show.validate_show(data):
        return redirect(f'shows/edit/{request.form["r_id"]}')
    Show.edit(data)
    return redirect('/shows')

#delete show
@app.route('/delete/<int:show_id>')
def deleteShow(show_id):
    data = {
        'id' : show_id
    }
    Show.delete(data)
    return redirect('/shows')