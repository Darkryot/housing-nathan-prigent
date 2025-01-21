from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2005@127.0.0.1:5432/house'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class House(db.Model):
    __tablename__ = "houses"
    house_id = db.Column(db.Integer, primary_key=True, unique=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    housing_median_age = db.Column(db.Integer)
    total_rooms = db.Column(db.Integer)
    total_bedrooms = db.Column(db.Integer)
    population = db.Column(db.Integer)
    households = db.Column(db.Integer)
    median_income = db.Column(db.Float)
    median_house_value = db.Column(db.Float)
    ocean_proximity = db.Column(db.String(255))


# Routes
@app.route('/houses', methods=['GET'])
def get_houses():
    houses = House.query.all()
    return jsonify([{
        "house_id": house.house_id,
        "longitude": house.longitude,
        "latitude": house.latitude,
        "housing_median_age": house.housing_median_age,
        "total_rooms": house.total_rooms,
        "total_bedrooms": house.total_bedrooms,
        "population": house.population,
        "households": house.households,
        "median_income": house.median_income,
        "median_house_value": house.median_house_value,
        "ocean_proximity": house.ocean_proximity,
    } for house in houses])


@app.route('/houses', methods=['POST'])
def add_house():
    data = request.json
    house = House(**data)
    db.session.add(house)
    db.session.commit()
    return jsonify({"message": "House added successfully!"}), 201


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)