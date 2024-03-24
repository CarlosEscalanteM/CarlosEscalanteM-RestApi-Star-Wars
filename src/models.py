from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(20), nullable=False)
    loyal_to = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    population = db.Column(db.Integer)

class Starship(db.Model):
    __tablename__ = "starship"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20))
    loyal_to = db.Column(db.String(20), nullable=False)

class FavoriteType(Enum):
    CHARACTER = "character"
    PLANET = "planet"
    STARSHIP = "starship" 

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relationship = db.relationship(User)
    favorite_character = db.relationship(Character)
    favorite_planet = db.relationship(Planet)
    favorite_starship = db.relationship(Starship)
    favorite_type = db.Column(db.Enum(FavoriteType), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"))
