from flask import request
from app import db
from app.api import api
from app.models import Planet, Player, Ship

# GET
@api.get('/players/<int:id>')
def get_player(id):
    player = db.get_or_404(Player, id)

    return player.to_dict()

# CREATE
@api.post('/players')
def create_player():
    data = request.get_json()

    player = Player(
        name = data["name"]
    )

    db.session.add(player)
    db.session.commit()

    return player.to_dict(), 201

# UPDATE
@api.put('/players/<int:id>')
def update_player(id):
    player = db.get_or_404(Player, id)

    data = request.get_json()

    db.get_or_404(Planet, data["home_planet_id"])

    player.name = data["name"]
    player.credits = data["credits"]
    player.home_planet_id = data["home_planet_id"]

    db.session.commit()

    return player.to_dict()

# DELETE
@api.delete('/players/<int:id>')
def delete_player(id):
    player = db.get_or_404(Player, id)

    db.session.delete(player)
    db.session.commit()

    return "", 204

# GET SHIPS
@api.get('/players/<int:id>/ships')
def get_player_ships(id):
    player = db.get_or_404(Player, id)

    query = db.select(Ship).where(Ship.player_id == player.id)
    ships = db.session.scalars(query).all()
    return [ship.to_dict() for ship in ships]
 
# CREATE
@api.post('/players/<int:id>/ships')
def create_ship(id):
    data = request.get_json()

    db.get_or_404(Player, id)

    ship = Ship(
        name=data["name"],
        fuel=data["fuel"],
        max_fuel=data["max_fuel"],
        player_id=id,
        x=data["x"],
        y=data["y"]
    )

    db.session.add(ship)
    db.session.commit()

    return ship.to_dict(), 201
