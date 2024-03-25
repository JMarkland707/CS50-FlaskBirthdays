import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# Create list of months
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]

# create list of days
DAYS = list(range(1, 32))

# Create list for years
YEARS = list(range(1900, 2025))

# Combine entries for birthday
#birthday = (f"{MONTHS} / {DAYS} / {YEARS}")

# Create dictionary for users who input their birthday
#USERS = {}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/deregister", methods=["POST"])
def deregister():

    #Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id =?", id)
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Access form data
        name = request.form.get("name")
        if not name:
            print("name is missing")
            return redirect("/")
        month = request.form.get("month")
        if not month:
            print("month is missing")
            return redirect("/")
        try:
            month = int(month)
        except ValueError:
            return redirect("/")
        if month < 0 or month > 12:
            return redirect("/")

        day = request.form.get("day")
        if not day:
            print("day is missing")
            return redirect("/")
        try:
            day = int(day)
        except ValueError:
            return redirect("/")
        if day < 0 or day > 31:
            return redirect("/")

        year = request.form.get("year")
        if not year:
            return redirect("/")
        try:
            year = int(year)
        except ValueError:
            return redirect("/")

        # Insert data into database
        db.execute("INSERT INTO birthdays (name, month, day, year) VALUES(?, ?, ?, ?)", name, month, day, year)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        #query all the birthdays
        birthdays = db.execute("SELECT * FROM birthdays")
        print(birthdays)
        return render_template("index.html", birthdays=birthdays)


