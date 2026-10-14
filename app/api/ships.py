from flask import request
from app import db
from app.api import api
from app.game import get_planet_at
from app.models import Planet, Player, Ship
from math import sqrt

# GET
@api.get('/ships/<int:id>')
def get_ship(id):
    ship = db.get_or_404(Ship, id)

    return ship.to_dict()

# GET PLAYER
@api.get('/ships/<int:id>/player')
def get_ship_player(id):
    ship = db.get_or_404(Ship, id)
    player = db.get_or_404(Player, ship.player_id)

    return player.to_dict()

# UPDATE
@api.put('/ships/<int:id>')
def update_ship(id):
    ship = db.get_or_404(Ship, id)

    data = request.get_json()

    db.get_or_404(Player, data["player_id"])

    ship.name = data["name"]
    ship.fuel = data["fuel"]
    ship.max_fuel = data["max_fuel"]
    ship.player_id = data["player_id"]

    db.session.commit()

    return ship.to_dict()

# DELETE
@api.delete('/ships/<int:id>')
def delete_ship(id):
    ship = db.get_or_404(Ship, id)

    db.session.delete(ship)
    db.session.commit()

    return "", 204

# MOVE
@api.post('/ships/<int:id>/move')
def move_ship(id):
    ship = db.get_or_404(Ship, id)

    data = request.get_json()

    distance = sqrt((data["x"] - ship.x) ** 2 + (data["y"] - ship.y) ** 2)

    if ship.fuel < distance:
        return {"error": "Not enough fuel."}, 400
    
    ship.fuel -= distance
    ship.x = data["x"]
    ship.y = data["y"]

    db.session.commit()

    return ship.to_dict()

# NEARBY
@api.get('/ships/<int:id>/nearby')
def get_nearby(id):
    ship = db.get_or_404(Ship, id)

    nearby = []

    ships = db.session.scalars(
        db.select(Ship).where(Ship.id != ship.id)
    ).all()

    planets = db.session.scalars(
        db.select(Planet)
    ).all()

    objects = ships + planets

    for obj in objects:
        distance = sqrt((obj.x - ship.x) ** 2 + (obj.y - ship.y) ** 2)
        if distance <= 10:
            item_dict = obj.to_dict()
            item_dict['type'] = type(obj).__name__.lower()
            nearby.append(item_dict)

    return nearby

# REFUEL
@api.post('/ships/<int:id>/refuel')
def refuel_ship(id):
    ship = db.get_or_404(Ship, id)
    player = db.get_or_404(Player, ship.player_id)
    planet = get_planet_at(ship)

    if planet is None:
        return {"error": "Ship is not at a planet."}, 400

    cost = ship.max_fuel - ship.fuel
    bought = min(cost, player.credits)

    player.credits -= bought
    ship.fuel += bought

    db.session.commit()
    return ship.to_dict()