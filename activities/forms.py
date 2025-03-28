import csv

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, DateField, IntegerRangeField, SubmitField
from wtforms.validators import NumberRange

from activities import calculations

class ActivityForm(FlaskForm):
    choices = ["Car", "Motorbike", "Van", "Flight", "Food"]
    activity = SelectField("activity", choices=choices)
    submit = SubmitField()

class FuelForm(FlaskForm):
    choices = ["Petrol", "Diesel", "LPG"]
    
    fuelType = SelectField("fuel_type", choices=choices)
    submit = SubmitField()


class CarSizeForm(FlaskForm):
    choices = ["Small", "Medium", "Large"]
    carSize = SelectField("car_size", choices=choices)
    submit = SubmitField()


class MotorbikeSizeForm(FlaskForm):
    choices = ["Small", "Medium", "Large"]
    motorbikeSize = SelectField("motorbike_size", choices=choices)
    submit = SubmitField()


class VanSizeForm(FlaskForm):
    choices = ["Small", "Medium", "Large"]
    vanSize = SelectField("van_size", choices=choices)
    submit = SubmitField()


class FlightForm(FlaskForm):
    choices = []
    with open("static/csv/airports.csv", newline="\n", encoding="utf-8") as airports:
        airportsReader = csv.reader(airports, delimiter=",")
        airportsList = list(airportsReader)
    
    for i in airportsList:
        choices.append(i[1] + " (" + i[2] + ")")
    
    startAirport = SelectField("start_airport", choices=choices)
    endAirport = SelectField("end_airport", choices=choices)
    submit = SubmitField()


class FoodForm(FlaskForm):
    choices = []
    with open("static/csv/foods.csv", newline="\n", encoding="utf-8") as foods:
        foodsReader = csv.reader(foods, delimiter=",")
        foodsList = list(foodsReader)
    
    for i in foodsList:
        choices.append(i[1])
    
    foodChoice = SelectField("food_choice", choices=choices)
    submit = SubmitField()


class FoodQuantityForm(FlaskForm):
    foodQuantity = IntegerField("food_quantity_output")
    submit = SubmitField()
    

class ActivityDateForm(FlaskForm):
    activityDate = DateField("date")
    submit = SubmitField()


class DistanceTravelledForm(FlaskForm):
    distanceTravelled = IntegerRangeField("distance_travelled", id="slider")
    distanceTravelledOutput = IntegerField("distance_travelled_output", id="slider-output")
    submit = SubmitField()
