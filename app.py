from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_webapp")


@app.route('/')
def index():
    marsCollection = mongo.db.marsCollection.find_one()
    return render_template('index.html', marsCollection=marsCollection)


@app.route('/scrape')
def scrape():
    marsCollection = mongo.db.marsCollection
    data = scrape_mars.scrape()
    marsCollection.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
