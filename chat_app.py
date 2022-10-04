import os
import json
from flask import Flask, request, abort, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

keyVal=0
msg = None

class logins(db.Model):
    id =        db.Column(db.String(25), primary_key=True)
    pw =        db.Column(db.String(25), nullable=False)
    email =     db.Column(db.String(25),nullable=False)
    loginStatus = db.Column(db.Integer, nullable=False)

class chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)
    content = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return '<Task %r>' % self.id

db.create_all()

# Setting key for chat
# If the database is empty key == 0, otherwise key = key+1 
f = db.session.query(chat).first() 
if f!=None:
    keyVal = db.session.query(chat).order_by(chat.id)[-1].id+1

# GET root, returns the login controller 
@app.route("/")
def default():
    return redirect(url_for("login_controller"))


# Login controller: handles login.html 
@app.route("/login/", methods=['GET', 'POST'])
def login_controller():
    global msg
    # CASE = Get the login page (GET)
    if request.method == "GET":
        if msg!=None:
            temp = msg
            msg = None
            return render_template("login.html", result=temp)
        # return the login page 
        return render_template("login.html")
    # CASE = Submit login form (POST)
    if request.method == "POST":
        # get the form fields 
        userLogin = request.form.get('user')
        userPass = request.form.get('pass')
        # are the fields empty?
        if userLogin == '' or userPass == '':
            return render_template("login.html", result="Login fields incomplete")
        # check if the user exists 
        exists = db.session.query(db.exists().where(logins.id == userLogin)).scalar()
        # user doesn't exist, return error message 
        if exists == False:
            return render_template("login.html", result="Username does not exist")
        # user exists, check if the password is correct 
        else:
            # get the password from the database 
            checkPass = logins.query.get_or_404(userLogin).pw
            # compare the two passwords 
            
            # incorrect password 
            if userPass != checkPass:   
                return render_template("login.html", result="Incorrect password")
            # correct credentials 
            user = logins.query.filter_by(id=userLogin).first()
            user.loginStatus = 1
            db.session.commit()
            return redirect(url_for("profile", username = user.id))



@app.route("/register/", methods =['GET', 'POST'])
def register_controller():
    global msg
    # requesting register page 
    if request.method == "GET":
        return render_template("register.html")
    # user submitting register page 
    if request.method == "POST":
        # get the user parameter 
        user = request.form.get('user')
        email = request.form.get('email')
        pass0 = request.form.get('pass0')
        pass1 = request.form.get('pass1')
        # check if any fields are empty 
        if user == '' or email == '' or pass0 == '' or pass1 == '':
            return render_template("register.html", failure="A field was left empty", u=user, e = email, p0 = pass0, p1=pass1)
        # check if the username has been taken 
        if db.session.query(db.exists().where(logins.id == user)).scalar() == True:
            return render_template("register.html", failure="That username has already been selected")
        # check if the passwords match 
        if pass0 != pass1:
            return render_template("register.html", failure="Passwords do not match", u=user, e = email, p0 = pass0, p1=pass1)
        # all requirements met 
        
        new_task = logins(id=user, pw= pass0, email = email,loginStatus= 0)
        db.session.add(new_task)
        db.session.commit()
        msg= "Account Successfully Generated"
        return redirect(url_for("login_controller"))

@app.route("/profile/<string:username>") 
def profile(username=None):

    user = logins.query.filter_by(id=username).first()
    if user==None:
        print("User does not exist")
        return redirect(url_for("login_controller"))
    if user.loginStatus == 0: 
        print("User currently not logged in ")
        return redirect(url_for("login_controller"))
    return render_template("chatPage.html", name=username)


@app.route("/logout/", methods =['GET', 'POST']) 
def unlogger(username=None):
    global msg 
    msg = "Successfully logged out"
    userLogin = request.form.get('signout')
    user = logins.query.filter_by(id=userLogin).first()
    user.loginStatus = 0
    db.session.commit()
    return render_template("logout.html")

@app.route("/new_message/", methods=["POST"]) 
def new_message():
    global keyVal
    username = request.form["username"]
    content = request.form["message"]
    new_task = chat(id=keyVal,name=username, content= content)
    db.session.add(new_task)
    db.session.commit()    
    result = db.session.query(chat).all()
    keyVal+=1
    print(len(result))
    ret=[]
    for i in result:
        s = i.name + ": " + i.content
        ret.append(s)
    return json.dumps(ret)

@app.route("/messages/") 
def messages():
    result = db.session.query(chat).all()
    ret=[]
    for i in result:
        s = i.name + ": " + i.content
        ret.append(s)
    return json.dumps(ret)
    

if __name__ == "__main__":
    app.run()
