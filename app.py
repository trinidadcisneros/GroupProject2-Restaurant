from flask import Flask, render_template
import data
import pymongo

# create instance of Flask app
app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/mars_db")
db = client.get_database()


# create route that renders index.html template
@app.route("/")
def index():



if __name__ == "__main__":
    app.run(debug=True)