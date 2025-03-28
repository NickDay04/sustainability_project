from datetime import date, timedelta
import random


def emissions(user_id):
    from models import Activity
    dieselCar = []
    for i in range(90):
        emission = random.randint(0, 71) / 10
        dieselCar.append(Activity(user_id, "Car", emission, date.today() - timedelta(i), fuel_type="Diesel"))
    foods = []
    for i in range(90):
        emission = random.randint(0, 67) / 10
        foods.append(Activity(user_id, "Food", emission, date.today() - timedelta(i)))
    return dieselCar, foods
