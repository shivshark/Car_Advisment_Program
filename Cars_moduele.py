""
cars_module.py
--------------
Holds the (expanded) car database and a function that returns
up to two matches based on user preferences.
"""

CARS_DB = [
    {
        "name": "Ford Explorer",
        "min_price": 30000,
        "max_price": 55000,
        "type": "commuter",
        "country": "usa",
        "seats": 7,
        "image_path": "images/ford_explorer.jpg"
    },
    {
        "name": "BMW M4",
        "min_price": 70000,
        "max_price": 100000,
        "type": "performance",
        "country": "germany",
        "seats": 4,
        "image_path": "images/bmw_m4.jpg"
    },
    {
        "name": "Honda Civic",
        "min_price": 20000,
        "max_price": 35000,
        "type": "commuter",
        "country": "japan",
        "seats": 5,
        "image_path": "images/honda_civic.jpg"
    },
    {
        "name": "Chevrolet Corvette",
        "min_price": 60000,
        "max_price": 90000,
        "type": "performance",
        "country": "usa",
        "seats": 2,
        "image_path": "images/corvette.jpg"
    },
    {
        "name": "Porsche 911",
        "min_price": 90000,
        "max_price": 200000,
        "type": "performance",
        "country": "germany",
        "seats": 4,
        "image_path": "images/porsche_911.jpg"
    },
    {
        "name": "Toyota Camry",
        "min_price": 25000,
        "max_price": 40000,
        "type": "commuter",
        "country": "japan",
        "seats": 5,
        "image_path": "images/toyota_camry.jpg"
    },
    {
        "name": "Honda Odyssey",
        "min_price": 32000,
        "max_price": 48000,
        "type": "commuter",
        "country": "japan",
        "seats": 7,
        "image_path": "images/honda_odyssey.jpg"
    },
    {
        "name": "Chevrolet Suburban",
        "min_price": 52000,
        "max_price": 75000,
        "type": "commuter",
        "country": "usa",
        "seats": 7,
        "image_path": "images/chevy_suburban.jpg"
    },
    {
        "name": "Tesla Model X",
        "min_price": 90000,
        "max_price": 130000,
        "type": "performance",
        "country": "usa",
        "seats": 6,
        "image_path": "images/tesla_modelx.jpg"
    },
    {
        "name": "Audi R8",
        "min_price": 150000,
        "max_price": 210000,
        "type": "performance",
        "country": "germany",
        "seats": 2,
        "image_path": "images/audi_r8.jpg"
    },
    {
        "name": "Lamborghini Huracan",
        "min_price": 200000,
        "max_price": 300000,
        "type": "performance",
        "country": "italy",
        "seats": 2,
        "image_path": "images/lamborghini_huracan.jpg"
    },
    {
        "name": "Ferrari 488",
        "min_price": 220000,
        "max_price": 350000,
        "type": "performance",
        "country": "italy",
        "seats": 2,
        "image_path": "images/ferrari_488.jpg"
    },
    {
        "name": "Maserati Quattroporte",
        "min_price": 100000,
        "max_price": 150000,
        "type": "performance",
        "country": "italy",
        "seats": 5,
        "image_path": "images/maserati_quattroporte.jpg"
    },
    {
        "name": "Nissan GT-R",
        "min_price": 115000,
        "max_price": 200000,
        "type": "performance",
        "country": "japan",
        "seats": 4,
        "image_path": "images/nissan_gtr.jpg"
    },
    {
        "name": "Toyota Highlander",
        "min_price": 35000,
        "max_price": 50000,
        "type": "commuter",
        "country": "japan",
        "seats": 7,
        "image_path": "images/toyota_highlander.jpg"
    },
    {
        "name": "Dodge Charger",
        "min_price": 30000,
        "max_price": 80000,
        "type": "performance",
        "country": "usa",
        "seats": 5,
        "image_path": "images/dodge_charger.jpg"
    },
]

def recommend_cars(
    budget: float,
    usage: str,
    country: str,
    seats: int,
    limit: int = 2
) -> list[str]:
    """
    Returns up to 'limit' matching car names from CARS_DB. 
    If none match, returns an empty list.

    :param budget: user budget in USD
    :param usage: "commuter" or "performance"
    :param country: "usa", "germany", "japan", "italy"
    :param seats: integer from 2 to 7
    :param limit: how many cars to return (default=2)
    :return: list of matching car names (empty if none)
    """
    usage = usage.lower().strip()
    country = country.lower().strip()

    matches: list[str] = []

    for car in CARS_DB:
        if car["min_price"] <= budget <= car["max_price"]:
            if car["type"] == usage:
                if car["country"] == country:
                    if car["seats"] == seats:
                        matches.append(car["name"])
                        if len(matches) == limit:
                            break

    return matches
