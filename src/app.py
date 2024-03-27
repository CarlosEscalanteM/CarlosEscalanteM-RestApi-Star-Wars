"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Starship
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialize_users = list(map(lambda user:user.serialize(),users))
    return jsonify(serialize_users), 200

@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialize_characters = list(map(lambda character:character.serialize(),characters))
    return jsonify(serialize_characters), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialize_planets = list(map(lambda planet:planet.serialize(),planets))
    return jsonify(serialize_planets), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    serialize_starships = list(map(lambda starship:starship.serialize(),starships))
    return jsonify(serialize_starships), 200

@app.route("/people/<int:people_id>")
def get_character(people_id):
    character = Character.query.get(people_id)
    return jsonify(character.serialize()), 200

@app.route("/planets/<int:planets_id>")
def get_planet(planets_id):
    planet = Planet.query.get(planets_id)
    return jsonify(planet.serialize()), 200

@app.route("/starships/<int:starships_id>")
def get_starship(starships_id):
    starship = Starship.query.get(starships_id)
    return jsonify(starship.serialize()), 200

@app.route("/users/favorites/<int:user_id>")
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    user_favorites = user.serialize() .get("favorites")
    return jsonify(user_favorites), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
