from app import db
from app.models import Ship, Planet
from math import sqrt

def get_planet_at(ship):
    planets = db.session.scalars(
        db.select(Planet)
    ).all()

    for obj in planets:
        distance = sqrt((obj.x - ship.x) ** 2 + (obj.y - ship.y) ** 2)
        if distance <= 1:
            return obj
    return None
