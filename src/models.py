from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorite")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # password and is_active not serialize for security purposes
            "favorites": [favorite.serialize() for favorite in self.favorites]

        }
class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(100), nullable=True, default="N/A")
    loyal_to = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "loyal_to": self.loyal_to,
            "height":self.height,
            "weight":self.weight,
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=True, default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "terrain": self.terrain,
        }

class Starship(db.Model):
    __tablename__ = "starship"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20))
    loyal_to = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race
            # do not serialize the password, its a security breach
        }

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
    
    def serialize(self):
        serialized_data = {"id": self.id, "favorite_type": self.favorite_type.value}
        if self.favorite_type == FavoriteType.CHARACTER and self.favorite_character:
            serialized_data["character"] = self.favorite_character.serialize()
        elif self.favorite_type == FavoriteType.PLANET and self.favorite_planet:
            serialized_data["planet"] = self.favorite_planet.serialize()
        elif self.favorite_type == FavoriteType.STARSHIP and self.favorite_starship:
            serialized_data["starship"] = self.favorite_starship.serialize()
            
        return serialized_data

