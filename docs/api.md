# API

## Players

### Get Player

`GET /api/players/<id>`

Returns information about a player.

### Create Player

`POST /api/players`

**Request:**

```json
{
    "name": "TestPlayer"
}
```

### Update Player

`PUT /api/players/<id>`

Updates a player's name, credits, and home planet

**Request:**

```json
{
    "name": "NewName",
    "credits": 15000,
    "home_planet_id": 2
}
```

### Delete Player

`DELETE /api/players/<id>`

Deletes a player.

### Get Player's Ships

`GET /api/players/<id>/ships`

Get the ships associated with a player

### Add Ship to Player

`POST /api/players/<id>/ships`

**Request:**

```json
{
    "name": "NewName",
    "fuel": 100
}
```



## Ships

### Get Ship

`GET /api/ships/<id>`

Returns information about a ship

### Get Ship's Player

`GET /api/ships/<id>/player`

Returns player associated with a ship

### Update Ship

`PUT /api/ships/<id>`

Updates a ship's name, fuel, and player id

**Request:**

```json
{
    "name": "NewName",
    "fuel": 100,
    "player_id": 1
}
```

### Delete Ship

`DELETE /api/ships/<id>`

Deletes a ship.