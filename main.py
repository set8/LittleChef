#pckgs
import pymongo
from mongodb import validateUser, getPantry, createUser, setPantry, getUserData

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
#built-in
from threading import Thread
from random import seed
from hashlib import sha256
import json

#file imports
from dish import Dish

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = seed() #will make data stored on filesystem encrypted and secure

app.config["SESSION_PERMANENT"] = True #User will remain logged in for time after browser close
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/") #this is the Home screen
def index():
    if not session.get("username"):
        return redirect("/login")

    return render_template('index.html')

@app.route("/login", methods= ["POST", "GET"])
def login(): #if not signed in, goes to login
    err = ""
    
    if request.method == "POST": #user submitted form
        username = request.form.get("username")
        hashpass = None if not request.form.get("password") else sha256(request.form.get("password").encode("utf-8")).hexdigest()

        validation = validateUser(username, hashpass)
        print(username, hashpass, validation, sep="\t")

        if not (username and hashpass):
            err = "Please fill out Username and Password fields"
        elif validation == -1:
            err = f"No registered account under {username}"
        elif validation == 0:
            err = "Password Incorrect"
        else: # login success
            session["username"] = request.form.get("username")
            return redirect("/")
    
    return render_template("login.html", err = err, isErr = (str(bool(err)))) #brings user to login page

@app.route("/signup", methods= ["POST", "GET"]) #TODO PLEASE TEST, PLEASE GOD
def signup(): #if not signed in, goes to login
    err = ""

    if request.method == "POST": #user submitted form
        username = request.form.get("username")
        hashpass = None if not request.form.get("password") else sha256(request.form.get("password").encode("utf-8")).hexdigest()
        age = request.form.get("age")

        allergens = request.form.get("allergens")
        diet = request.form.get("diet")

        validation = validateUser(username, hashpass)
        
        if not (username and age and hashpass): #failed
            err = "Please fill out Username, Password, and Age fields"
        elif not age.isdigit() or len([x for x in age if x in "-.,"]) > 0:
            err = "Age must be an integer number"
        elif validation == 0 or validation == 1:
            err = "User account already exists, please log in"
        
        else: #everything is peachy :3
            session["username"] = username #can now navigate the website
            createUser(username, hashpass, "" if not allergens else allergens.split(","), diet, age, {"":""}) #upload to mongo
            return redirect("/")

    return render_template("signup.html", err = err, isErr = (str(bool(err)))) #brings user to signup

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login") #back to login screen

@app.route("/dishes")
def dishes():

    if not session.get("username"): #not signed in
        return redirect("/login")

    Dish.dishes = [] #reset class attribute for future assignment
    data = getUserData(session.get("username"))
    
    if data is not None:
        userdata = {
            "pantry": data[3],
            "allergies": (data[0] if type(data[0]) is not list else ",".join(data[0])),
            "diet" : data[1],
            "age" : data[2]
        }

        t1 = Thread(target=Dish, args=userdata)
        t2 = Thread(target=Dish, args=userdata)
        t3 = Thread(target=Dish, args=userdata) #have the dishes wait for join() in the class variable dishes
        
        ts = (t1, t2, t3)
        [x.start() for x in ts]
        [x.join() for x in ts] # maybe pre-process new batch for refresh too

        d1, d2, d3 = Dish.dishes #unpack
        
        return render_template("dishes.html", d1Name = d1.name, d2Name = d2.name, d3Name = d3.name, d1Imgage = d1.image, d2Image = d2.image, d3Image = d3.image, 
                            d1Instructions = d1.instructions, d2Instructions = d2.instructions, d3Instructions = d3.instructions,
                            d1Ingredients = d1.ingredients, d2Ingredients = d2.ingredients, d3Ingredients = d3.ingredients)
    else:
        return "Please add some foods to your pantry before searching for recipies!"
@app.route("/pantry")
def pantry():

    if not session.get("username"): #not signed in
        return redirect("/login")
 
    pantry = getPantry(session.get("username"))
    foods, quantities = ["", ""] if not pantry else pantry.items()
    
    return render_template("pantry.html", foods = foods, quantities = quantities, zip=zip)

@app.route("/pantryUploadForm", methods = ["POST", "GET"])
def uploadForm():
    if not session.get("username"): #not signed in
        return redirect("/login")

    if request.method == "POST":
        foodName = request.form.get("foodName") #returns the name of the food item
        foodQuantityNumber = request.form.get("quantityNumber") #returns the number of (unit of measure) the user has of a certain foodstuff
        foodQuantityMeasure = request.form.get("quantityMeasure") #returns the unit of measure for which the user has a quantity of a given foodstuff
        
        setPantry(session['username'], foodName, f"{foodQuantityNumber} {foodQuantityMeasure}") #overwrites pre-existing foodstuffs
        return redirect("/pantryUploadForm") #allows user to resubmit without having to erase previous submission

    return render_template("/pantryUploadForm.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8081)