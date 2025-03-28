from datetime import datetime
from flask import session


'''
Test ID: WB06
Tests normal car add activity gets stored in session data
'''
def test_add_car_normal(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Car",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Car"

    data2 = {
        "fuelType": "Petrol",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["fuel_type"]) == "Petrol"

    data3 = {
        "carSize": "Medium",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["car_size"]) == "Medium"

    data4 = {
        "distanceTravelled": "44",
        "distanceTravelledOutput": "44",
        "submit": "Submit"
    }
    response4 = client.post("/activities/add_activity", data=data4)
    assert response4.status_code == 200
    assert str(session["distance_travelled"]) == "44"

    data5 = {
        "activityDate": "2024-05-30",
        "submit": "Submit"
    }
    response5 = client.post("/activities/add_activity", data=data5)
    assert response5.status_code == 302
    assert datetime(session["activity_date"].year, session["activity_date"].month, session["activity_date"].day) == datetime(2024, 5, 30)


'''
Test ID: WB07
Tests erroneous value in distance travelled for car add activity throws error
'''
def test_add_car_erroneous(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Car",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Car"

    data2 = {
        "fuelType": "Petrol",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["fuel_type"]) == "Petrol"

    data3 = {
        "carSize": "Medium",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["car_size"]) == "Medium"

    data4 = {
        "distanceTravelled": "fail",
        "distanceTravelledOutput": "fail",
        "submit": "Submit"
    }
    response4 = client.post("/activities/add_activity", data=data4)
    assert response4.status_code == 200
    assert str(session["distance_travelled"]) == str(None)

    data5 = {
        "activityDate": "2024-05-29",
        "submit": "Submit"
    }
    try:
        client.post("/activities/add_activity", data=data5)
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for *: 'float' and 'NoneType'"


'''
Test ID: WB08
Tests normal flight add activity gets stored in session data
'''
def test_add_flight_normal(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Flight",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Flight"

    data2 = {
        "startAirport": "Heathrow+Airport+(LHR)",
        "endAirport": "Amsterdam+Airport+Schiphol+(AMS)",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["start_airport"]) == "Heathrow+Airport+(LHR)"
    assert str(session["end_airport"]) == "Amsterdam+Airport+Schiphol+(AMS)"

    data3 = {
        "activityDate": "2024-05-28",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 302
    assert datetime(session["activity_date"].year, session["activity_date"].month, session["activity_date"].day) == datetime(2024, 5, 28)


'''
Test ID: WB09
Tests normal motorbike add activity gets stored in session data
'''
def test_add_motorbike_normal(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Motorbike",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Motorbike"

    data2 = {
        "motorbikeSize": "Medium",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["motorbike_size"]) == "Medium"

    data3 = {
        "distanceTravelled": "23",
        "distanceTravelledOutput": "23",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["distance_travelled"]) == "23"

    data4 = {
        "activityDate": "2024-05-27",
        "submit": "Submit"
    }
    response4 = client.post("/activities/add_activity", data=data4)
    assert response4.status_code == 302
    assert datetime(session["activity_date"].year, session["activity_date"].month, session["activity_date"].day) == datetime(2024, 5, 27)


'''
Test ID: WB10
Tests erroneous value in distance travelled for motorbike add activity throws type error.
'''
def test_add_motorbike_erroneous(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Motorbike",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Motorbike"

    data2 = {
        "motorbikeSize": "Medium",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["motorbike_size"]) == "Medium"

    data3 = {
        "distanceTravelled": "faill",
        "distanceTravelledOutput": "faill",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["distance_travelled"]) == str(None)

    data4 = {
        "activityDate": "2024-05-26",
        "submit": "Submit"
    }
    try:
        client.post("/activities/add_activity", data=data4)
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for *: 'float' and 'NoneType'"



'''
Test ID: WB11
Tests normal van add activity gets stored in session data
'''
def test_add_van_normal(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Van",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Van"

    data2 = {
        "vanSize": "Medium",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["van_size"]) == "Medium"

    data3 = {
        "distanceTravelled": "79",
        "distanceTravelledOutput": "79",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["distance_travelled"]) == "79"

    data4 = {
        "activityDate": "2024-05-25",
        "submit": "Submit"
    }
    response4 = client.post("/activities/add_activity", data=data4)
    assert response4.status_code == 302
    assert datetime(session["activity_date"].year, session["activity_date"].month, session["activity_date"].day) == datetime(2024, 5, 25)


'''
Test ID: WB12
Tests erroneous value in distance travelled for van add activity throws type error.
'''
def test_add_van_erroneous(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Van",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Van"

    data2 = {
        "vanSize": "Medium",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["van_size"]) == "Medium"

    data3 = {
        "distanceTravelled": "failforvan",
        "distanceTravelledOutput": "failforvan",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["distance_travelled"]) == str(None)

    data4 = {
        "activityDate": "2024-05-24",
        "submit": "Submit"
    }
    try:
        client.post("/activities/add_activity", data=data4)
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for *: 'float' and 'NoneType'"


'''
Test ID: WB13
Tests normal food add activity gets stored in session data
'''
def test_add_food_normal(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Food",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Food"

    data2 = {
        "foodChoice": "Dark Chocolate",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["food_choice"]) == "Dark Chocolate"

    data3 = {
        "foodQuantity": "500",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["food_quantity"]) == "500"

    data4 = {
        "activityDate": "2024-05-23",
        "submit": "Submit"
    }
    response4 = client.post("/activities/add_activity", data=data4)
    assert response4.status_code == 302
    assert datetime(session["activity_date"].year, session["activity_date"].month, session["activity_date"].day) == datetime(2024, 5, 23)


'''
Test ID: WB14
Tests erroneous value in food quantity in food add activity throws type error.
'''
def test_add_food_erroneous(client):
    client.get("/activities/add_activity")
    session.clear()
    data1 = {
        "activity": "Food",
        "submit": "Submit"
    }
    response1 = client.post("/activities/add_activity", data=data1)
    assert response1.status_code == 200
    assert session["activity"] == "Food"

    data2 = {
        "foodChoice": "Dark Chocolate",
        "submit": "Submit"
    }
    response2 = client.post("/activities/add_activity", data=data2)
    assert response2.status_code == 200
    assert str(session["food_choice"]) == "Dark Chocolate"

    data3 = {
        "foodQuantity": "hahafail",
        "submit": "Submit"
    }
    response3 = client.post("/activities/add_activity", data=data3)
    assert response3.status_code == 200
    assert str(session["food_quantity"]) == str(None)

    data4 = {
        "activityDate": "2024-05-22",
        "submit": "Submit"
    }
    try:
        client.post("/activities/add_activity", data=data4)
    except TypeError as e:
        assert str(e) == "unsupported operand type(s) for *: 'float' and 'NoneType'"