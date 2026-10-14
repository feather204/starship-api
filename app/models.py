from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=10000)
    home_planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "credits": self.credits,
            "home_planet_id": self.home_planet_id
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    population = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(256))
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "description": self.description,
            "x": self.x,
            "y": self.y
        }

class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    fuel = db.Column(db.Float, nullable=False, default=100.0)
    max_fuel = db.Column(db.Float, nullable=False, default=100.0)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "fuel": self.fuel,
            "max_fuel": self.max_fuel,
            "player_id": self.player_id,
            "x": self.x,
            "y": self.y
        }