from flask import request
from app import db
from app.api import api
from app.models import Planet

# GET
@api.get("/planets/<int:id>")
def get_planet(id):
    planet = db.get_or_404(Planet, id)

    return planet.to_dict()

# GET ALL
@api.get("/planets")
def get_planets():
    planets = db.session.scalars(db.select(Planet)).all()

    return [planet.to_dict() for planet in planets]

# CREATE
@api.post("/planets")
def create_planet():
    data = request.get_json()

    planet = Planet(
        name=data["name"],
        population=data["population"],
        description=data["description"],
        x=data["x"],
        y=data["y"]
    )

    db.session.add(planet)
    db.session.commit()

    return planet.to_dict(), 201

# UPDATE
@api.put('/planets/<int:id>')
def update_planet(id):
    planet = db.get_or_404(Planet, id)

    data = request.get_json()

    planet.name = data["name"]
    planet.population = data["population"]
    planet.description = data["description"]

    db.session.commit()

    return planet.to_dict()

# DELETE
@api.delete('/planets/<int:id>')
def delete_planet(id):
    planet = db.get_or_404(Planet, id)

    db.session.delete(planet)
    db.session.commit()

    return "", 204
