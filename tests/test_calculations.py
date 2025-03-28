# # test_calculations.py

# import pytest
# import pandas as pd
# import numpy as np
# from activities.calculations import (calculate_car_fuel, calculate_flight_distance, calculate_flight_emissions,
#                                      calculate_motorbike_emissions, calculate_van_emissions, calculate_food_emissions,
#                                      analyse_activity)

# # Mock data for testing purposes
# @pytest.fixture
# def mock_airports_csv(monkeypatch):
#     data = {
#         "airport-code": ["AAA", "BBB"],
#         "latitude": [0.0, 10.0],
#         "longitude": [0.0, 10.0]
#     }
#     df = pd.DataFrame(data)
#     monkeypatch.setattr(pd, "read_csv", lambda _: df)

# @pytest.fixture
# def mock_foods_csv(monkeypatch):
#     data = {
#         "product": ["apple", "banana"],
#         "emissions": [0.3, 0.2]
#     }
#     df = pd.DataFrame(data)
#     monkeypatch.setattr(pd, "read_csv", lambda _: df)

# @pytest.fixture
# def mock_emission_stats_csv(monkeypatch):
#     data = {
#         "category": ["car", "flight"],
#         "value": [0.2, 0.3]
#     }
#     df = pd.DataFrame(data)
#     monkeypatch.setattr(pd, "read_csv", lambda _: df)


# # Test calculate_car_fuel
# def test_calculate_car_fuel_normal():
#     assert calculate_car_fuel("Diesel", "Small", 100) == 13.9
#     assert calculate_car_fuel("Petrol", "Medium", 50) == 8.9
#     assert calculate_car_fuel("LPG", "Large", 200) == 53.8

# def test_calculate_car_fuel_boundary():
#     assert calculate_car_fuel("Diesel", "Small", 0) == 0
#     assert calculate_car_fuel("Petrol", "Large", 0) == 0

# def test_calculate_car_fuel_erroneous():
#     with pytest.raises(Exception):
#         calculate_car_fuel("Electric", "Medium", 100)

# # Test calculate_flight_distance
# def test_calculate_flight_distance_normal(mock_airports_csv):
#     distance = calculate_flight_distance("AAA", "BBB")
#     assert distance > 0

# def test_calculate_flight_distance_boundary(mock_airports_csv):
#     distance = calculate_flight_distance("AAA", "AAA")
#     assert distance == 0

# def test_calculate_flight_distance_erroneous(mock_airports_csv):
#     with pytest.raises(KeyError):
#         calculate_flight_distance("AAA", "CCC")

# # Test calculate_flight_emissions
# def test_calculate_flight_emissions_normal():
#     assert calculate_flight_emissions(500) == 0.251 * 500
#     assert calculate_flight_emissions(1500) == 0.195 * 1500

# def test_calculate_flight_emissions_boundary():
#     assert calculate_flight_emissions(1000) == 0.251 * 1000

# # Test calculate_motorbike_emissions
# def test_calculate_motorbike_emissions_normal():
#     assert calculate_motorbike_emissions(100, "Small") == 8.3
#     assert calculate_motorbike_emissions(200, "Medium") == 20.2
#     assert calculate_motorbike_emissions(300, "Large") == 39.6

# def test_calculate_motorbike_emissions_boundary():
#     assert calculate_motorbike_emissions(0, "Small") == 0

# def test_calculate_motorbike_emissions_erroneous():
#     with pytest.raises(Exception):
#         calculate_motorbike_emissions(100, "Extra Large")

# # Test calculate_van_emissions
# def test_calculate_van_emissions_normal():
#     assert calculate_van_emissions("Small", "Diesel", 100) == 14.2
#     assert calculate_van_emissions("Medium", "Petrol", 100) == 19.5
#     assert calculate_van_emissions("Large", "LPG", 100) == 25.5

# def test_calculate_van_emissions_boundary():
#     assert calculate_van_emissions("Small", "Diesel", 0) == 0

# def test_calculate_van_emissions_erroneous():
#     with pytest.raises(Exception):
#         calculate_van_emissions("Small", "Electric", 100)

# # Test calculate_food_emissions
# def test_calculate_food_emissions_normal(mock_foods_csv):
#     assert calculate_food_emissions("apple", 100) == 0.03
#     assert calculate_food_emissions("banana", 200) == 0.04

# def test_calculate_food_emissions_boundary(mock_foods_csv):
#     assert calculate_food_emissions("apple", 0) == 0

# def test_calculate_food_emissions_erroneous(mock_foods_csv):
#     with pytest.raises(KeyError):
#         calculate_food_emissions("orange", 100)

# # Test analyse_activity
# def test_analyse_activity_normal(mock_emission_stats_csv):
#     assert analyse_activity("car", 20, 1) == 100.0
#     assert analyse_activity("flight", 60, 1) == 200.0

# def test_analyse_activity_boundary(mock_emission_stats_csv):
#     assert analyse_activity("car", 0, 1) == 0.0

# def test_analyse_activity_erroneous(mock_emission_stats_csv):
#     with pytest.raises(KeyError):
#         analyse_activity("bus", 100, 1)
