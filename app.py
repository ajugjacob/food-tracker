import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    carbo = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_name = request.form.get('name').encode('ascii','ignore')
        new_carb = request.form.get('carbohydrates')
        new_fat = request.form.get('fat')
        new_cal = request.form.get('calories')
        new_prot = request.form.get('proteins')
        if new_name:
            existing_name = Tracker.query.filter_by(name=new_name).first()
            if not existing_name:
                new_track_obj = Tracker(name=new_name, carbo=new_carb, fat=new_fat, calories=new_cal, proteins=new_prot)
                db.session.add(new_track_obj)
                db.session.commit()
    foods = Tracker.query.all()
    food_tracker=[]
    for food in foods:
        foodtracker = {
            "name": food.name.encode('ascii','ignore'),
            "carbohydrate": food.carbo,
            "fat": food.fat,
            "calories": food.calories,
            "proteins": food.proteins
        }
        food_tracker.append(foodtracker)
    return render_template('index.html', food_tracker=food_tracker)

@app.route('/add', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        return redirect(url_for('index'), code='307')
    return render_template('add-item.html')

if __name__ == '__main__':
    port = int(os.environ.get("port",5000))
    app.run(threaded=True)