from flask import Flask, render_template, redirect, request, session

@app.route("/", methods="POST") #THIS IS TECHNICALLY THE HOME PAGE, USER MUST BE SIGNED IN TO USE APPLICATION
def login():
    pass
    if request.method == "POST":
        #must in HTML have form block with input tag 
        session["username"] = request.form.get("name");

@app.route("/home")
def home():
    return render_template("home.html")