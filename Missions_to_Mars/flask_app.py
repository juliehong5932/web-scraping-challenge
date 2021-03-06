from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo=PyMongo(app)

@app.route('/')
def index():
    results = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=results)
    
@app.route('/scrape')
def scrape():
    data=scrape_mars.scrape_all()
    mongo.db.mars.update({}, mars_data, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run()
