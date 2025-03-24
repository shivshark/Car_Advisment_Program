"""
cars_module.py
--------------
This module holds the car database and provides a function to recommend a car
based on user preferences: budget, type, country, and seating needs.
"""

from typing import Optional

# Sample database of cars
# Expand or modify these entries to suit your project.
CARS_DB = [
    {
        "name": "Ford Explorer",
        "min_price": 30000,
        "max_price": 55000,
        "type": "commuter",
        "country": "usa",
        "seats": 7
    },
    {
        "name": "BMW M4",
        "min_price": 70000,
        "max_price": 100000,
        "type": "performance",
        "country": "germany",
        "seats": 4
    },
    {
        "name": "Honda Civic",
        "min_price": 20000,
        "max_price": 35000,
        "type": "commuter",
        "country": "japan",
        "seats": 5
    },
    {
        "name": "Chevrolet Corvette",
        "min_price": 60000,
        "max_price": 90000,
        "type": "performance",
        "country": "usa",
        "seats": 2
    },
    {
        "name": "Porsche 911",
        "min_price": 90000,
        "max_price": 200000,
        "type": "performance",
        "country": "germany",
        "seats": 4
    },
    {
        "name": "Toyota Camry",
        "min_price": 25000,
        "max_price": 40000,
        "type": "commuter",
        "country": "japan",
        "seats": 5
    },
    # Add more cars as desired
]

def recommend_car(budget: float, usage: str, country: str, seats: int) -> Optional[str]:
    """
    Recommends a car from CARS_DB that matches the user's preferences.
    
    :param budget: The user's maximum budget.
    :param usage: "performance" or "commuter"
    :param country: e.g., "usa", "germany", "japan"
    :param seats: how many seats the user wants
    :return: The name of a recommended car, or None if no match is found.
    """
    usage = usage.lower().strip()
    country = country.lower().strip()

    for car in CARS_DB:
        # Check price range
        if car["min_price"] <= budget <= car["max_price"]:
            # Check usage type
            if car["type"] == usage:
                # Check country
                if car["country"] == country:
                    # Check seating
                    if car["seats"] == seats:
                        return car["name"]
                    
    # If no car in the database matches the user's preferences:
    return None