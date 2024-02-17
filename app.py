from flask import Flask, render_template, url_for, flash,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrete'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Cafe_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    picture_url = db.Column(db.String(255))
    wifi_status = db.Column(db.Boolean, default=False)



@app.route("/")
def home():
    all_cafes = Cafe_db.query.all()

    return render_template('index.html', all_cafes = all_cafes)

@app.route("/add_cafe", methods=["GET","POST"])
def add_cafe():

    if request.method == "POST":
        name = request.form['cafe_name']
        city = request.form['city']
        address = request.form['address']
        lat = request.form['lat']
        long = request.form['long']
        picture_url = request.form['picture_url']

        if request.form['wifi_status'] == "on":
            wifi_status = True
        else:
            wifi_status = False

        cafe_to_be_added = Cafe_db(name= name,city =city,
                                   address = address,lat = lat,long = long,
                                   picture_url = picture_url,wifi_status= wifi_status)

        db.session.add(cafe_to_be_added)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_cafe.html')





if __name__ == "__main__":
    app.run(debug=True)
