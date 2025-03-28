# -*- coding: utf-8 -*-
"""
    activities/calculations.py
    ~~~~~~~~~~~~~

    providing utility functions for activities related logic.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""

import pandas as pd
import numpy as np

# using fuel consumption per km
def calculate_car_fuel(fuel_type, car_size, distance):
    if fuel_type == "Diesel":
        if car_size == "Small":
            return 0.139 * distance
        elif car_size == "Medium":
            return 0.167 * distance
        else: # large
            return 0.208 * distance
    elif fuel_type == "Petrol":
        if car_size == "Small":
            return 0.14 * distance
        elif car_size == "Medium":
            return 0.178 * distance
        else: # large
            return 0.272 * distance
    else: # lpg
        if car_size == "Small":
            return 0.176 * distance
        elif car_size == "Medium":
            return 0.197 * distance
        else: # large
            return 0.269 * distance


# Given the airport codes for start and end, calculate the distance between the two airports
def calculate_flight_distance(start, end):
    airports = pd.read_csv("static/csv/airports.csv")
    phi1 = np.radians(airports[airports["airport-code"] == start]["latitude"].item())
    phi2 = np.radians(airports[airports["airport-code"] == end]["latitude"].item())
    delta_phi = phi2-phi1

    lambda1 = np.radians(airports[airports["airport-code"] == start]["longitude"].item())
    lambda2 = np.radians(airports[airports["airport-code"] == end]["longitude"].item())
    delta_lambda = lambda2-lambda1

    a = np.sin(np.half(delta_phi)) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(np.half(delta_lambda)) ** 2

    c = np.arctan2(np.sqrt(a), np.sqrt(1-a))

    R = 6371 # radius of earth in km

    d = R * c # distance between start and end

    return d


def calculate_flight_emissions(flight_distance):
    if flight_distance < 1000:
        return 0.251 * flight_distance
    else:
        return 0.195 * flight_distance
    

def calculate_motorbike_emissions(distance_travelled, size):
    if size.lower() == "small":
        return 0.083 * distance_travelled
    elif size.lower() == "medium":
        return 0.101 * distance_travelled
    else: # large
        return 0.132 * distance_travelled


def calculate_van_emissions(size, fuel_type, distance):
    if fuel_type == "Diesel":
        if size == "Small":
            return 0.142 * distance
        elif size == "Medium":
            return 0.174 * distance
        else: # large
            return 0.253 * distance
    elif fuel_type == "Petrol":
        if size == "Small":
            return 0.182 * distance
        elif size == "Medium":
            return 0.195 * distance
        else: # large
            return 0.314 * distance
    else: # lpg
        return 0.255 * distance


def calculate_food_emissions(food, weight):
    foods = pd.read_csv("static/csv/foods.csv")
    emissions_per_weight = foods[foods["product"] == food]["emissions"].item() / 1000
    return emissions_per_weight * weight

def analyse_activity(activity, emission, time_frame):
    emission_stats = pd.read_csv("static/csv/emission_stats.csv")
    average = float(emission_stats[emission_stats["category"] == activity.lower()]["value"].item()) * int(time_frame)
    return round((emission / average) * 100, 1)
