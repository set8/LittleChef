from flask import Flask, render_template, redirect, request, session
from flask_session import Session

from random import seed
from hashlib import sha256

app = Flask(__name__)
app.secret_key = seed() #will make data stored on filesystem encrypted and secure

app.config["SESSION_PERMANENT"] = True #User will remain logged in for time after browser close
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/") #this is the Home screen
def index(): #will default to home if signed in

    if not session.get("username"):
        return redirect("/login")

    return render_template('index.html')

@app.route("/login", methods= ["POST", "GET"])
def login(): #if not signed in, goes to login

    if request.method == "POST": #user submitted form
        # if usr not in users: meaning that user doesn't alreaady exist -> redirect them to sign-up
        # if login(usr, sha256(pass.encode("utf-8")).hexdigest()): meaning that the entered password is valid for a pre-existing user 
        session["username"] = request.form.get("username")
        return redirect("/")

    return render_template("dishes.html") #brings user to dishes for testing TODO change

@app.route("/signup", methods= ["POST", "GET"])
def signup(): #if not signed in, goes to login

    if request.method == "POST": #user submitted form
        # if usr not in users: meaning that user doesn't alreaady exist -> redirect them to sign-up
        # if login(usr, sha256(pass.encode("utf-8")).hexdigest()): meaning that the entered password is valid for a pre-existing user 
        session["username"] = request.form.get("username")
        # store(sha256(request.form.get("pw").encode("uft-8")).hexdigest())
        return redirect("/")

    return render_template("login.html") #brings user to login

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/") #back to login screen

@app.route("/dishes")
def dishes():

    # if not session.get("username"): #not signed in
    #     return redirect("/login") TODO undo

    # dishes = getDishes(session.userData)
    # dish = next(dishes)

    render_template("dishes.html") #TODO include 3 dishes

@app.route("/pantry")
def pantry():
    if not session.get("username"): #not signed in
        return redirect("/login")

    return render_template(pantry)
    
@app.route("/pantryUploadCamera")
def uploadCamera():
    if not session.get("username"): #not signed in
        return redirect("/login")
    
    return render_template("pantryUploadCamera.html")

@app.route("/pantryUploadForm", methods = ["POST", "GET"])
def uploadForm():
    if not session.get("username"): #not signed in
        return redirect("/login")

    if request.method == "POST":
        foodName = request.form.get("name") #returns the name of the food item
        foodQuantityNumber = request.form.get("quantityNumber") #returns the number of (unit of measure) the user has of a certain foodstuff
        foodQuantityMeasure = request.form.get("quantityMeasure") #returns the unit of measure for which the user has a quantity of a given foodstuff

        if foodName in session["userData"]["pantry"]: #TODO decide whether to override pre-existing counts or to add to it
            pass

        session["userData"]["pantry"][foodName] = f"{foodQuantityNumber} {foodQuantityMeasure}" #overwrites pre-existing foodstuffs
        return redirect("/pantryUploadForm.html") #allows user to resubmit without having to erase previous submission

    return render_template("/pantryUploadForm")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port = 8081)