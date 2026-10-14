import requests

BASE_URL = "http://127.0.0.1:5000/api"

def get_planets():
    response = requests.get(f"{BASE_URL}/planets")
    planets = response.json()
    print("╔═════════════════════════╦════════╗")
    for index, planet in enumerate(planets):
        print(f"║ PLANET : {planet['name']:<14} ║ {planet['x']:<2}, {planet['y']:<2} ║")
        if index < len(planets) - 1:
            print("╠═════════════════════════╬════════╣")
        else:
            print("╚═════════════════════════╩════════╝")
        
def get_player(id):
    response = requests.get(f"{BASE_URL}/players/{id}")
    if response.status_code != 200:
        print(f"Error: Player {id} not found.")
        return
    player = response.json()
    print("╔══════════════════════════════════╗")
    print(f"║ PLAYER  : {player['name']:<22} ║")
    print("╠══════════════════════════════════╣")
    print(f"║ ID      : {player['id']:<22} ║")
    print(f"║ CRED    : {player['credits']:<22.1f} ║")
    print(f"║ HOME_ID : {player['home_planet_id'] or 'NONE':<22} ║")
    print("╚══════════════════════════════════╝")

def get_ship(id):
    response = requests.get(f"{BASE_URL}/ships/{id}")
    if response.status_code != 200:
        print(f"Error: Ship {id} not found.")
        return
    ship = response.json()
    print("╔══════════════════════════════════╗")
    print(f"║ SHIP    : {ship['name']:<22} ║")
    print("╠══════════════════════════════════╣")
    print(f"║ ID      : {ship['id']:<22} ║")
    print(f"║ OWNER   : {ship['player_id']:<22} ║")
    print(f"║ FUEL    : {ship['fuel']:<14.1f} {ship['fuel'] / ship['max_fuel'] * 100:>6.1f}% ║")
    print(f"║ POS     : ({ship['x']:.1f}, {ship['y']:.1f}){' ':<11}║")
    print("╚══════════════════════════════════╝")

def get_nearby(id):
    response = requests.get(f"{BASE_URL}/ships/{id}/nearby")
    if response.status_code != 200:
        print(f"Error: Ship {id} not found.")
        return
    
    nearby = response.json()
    
    if nearby is None or len(nearby) == 0:
        print(f"Error: Nothing found near ship {id}.")
        return
    
    print("╔═════════════════════════╦══════════════╗")
    for index, item in enumerate(nearby):
        print(f"║ {item['type'].upper():<7}: {item['name']:<14} ║ {item['x']:>5.1f}, {item['y']:<5.1f} ║")
        if index < len(nearby) - 1:
            print("╠═════════════════════════╬══════════════╣")
        else:
            print("╚═════════════════════════╩══════════════╝")

def move_ship(id, x, y):
    response = requests.get(f"{BASE_URL}/ships/{id}")
    if response.status_code != 200:
        print(f"Error: Ship {id} not found.")
        return
    ship = response.json()
    old_x, old_y = ship['x'], ship['y']
    old_fuel = ship['fuel']
    response = requests.post(f"{BASE_URL}/ships/{id}/move", json={"x": x, "y": y})
    if response.status_code == 200:
        ship = response.json()
        print("╔══════════════════════════════════════╗")
        print(f"║ SHIP  : {ship['name']:<28} ║")
        print("╠══════════════════════════════════════╣")
        print(f"║ POS   : {old_x:>5.1f}, {old_y:<5.1f} -> {ship['x']:>5.1f}, {ship['y']:<5.1f} ║")
        print(f"║ FUEL  : {old_fuel:<6.1f} units -> {ship['fuel']:<6.1f} units ║")
        print("╚══════════════════════════════════════╝")
    else:
        print(f"Error: {response.json()['error']}\n")

def refuel_ship(id):
    response = requests.get(f"{BASE_URL}/ships/{id}")
    if response.status_code != 200:
        print(f"Error: Ship {id} not found.")
        return
    ship = response.json()
    old_fuel = ship['fuel']
    player = requests.get(f"{BASE_URL}/players/{response.json()['player_id']}").json()
    old_credits = player['credits']

    response = requests.post(f"{BASE_URL}/ships/{id}/refuel")

    if response.status_code == 200:
        ship = response.json()
        player = requests.get(f"{BASE_URL}/players/{response.json()['player_id']}").json()
        print("╔════════════════════════════════════════╗")
        print(f"║ SHIP    : {ship['name']:<28} ║")
        print("╠════════════════════════════════════════╣")
        print(f"║ FUEL    : {old_fuel:>6.1f} units -> {ship['fuel']:<6.1f} units ║")
        print(f"║ CREDITS : {old_credits:>12.1f} -> {player['credits']:<10.1f}   ║")
        print("╚════════════════════════════════════════╝")
    else:
        print(f"Error: {response.json()['error']}\n")

while True:
    choice = input("> ")
    words = choice.split()

    if not words:
        continue

    if words[0] == "planets":
        get_planets()
    elif words[0] == "player":
        if len(words) == 2:
            get_player(int(words[1]))
        else:
            print("Usage: player <id>")
    elif words[0] == "ship":
        if len(words) == 2:
            get_ship(int(words[1]))
        else:
            print("Usage: ship <id>")
    elif words[0] == "nearby":
        if len(words) == 2:
            get_nearby(int(words[1]))
        else:
            print("Usage: nearby <id>")
    elif words[0] == "move":
        if len(words) == 4:
            move_ship(int(words[1]), float(words[2]), float(words[3]))
        else:
            print("Usage: move <id> <x> <y>")
    elif words[0] == "refuel":
        if len(words) == 2:
            refuel_ship(int(words[1]))
        else:
            print("Usage: refuel <id>")