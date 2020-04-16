from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars.py

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    data = mongo.db.mars_data.find_one()
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scraper():
    data = mongo.db.mars_data
   
   
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)