# -*- coding: utf-8 -*-
"""
    main/views.py
    ~~~~~~~~~~~~~

    Contains routing and rendering for all activities pages.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""
from datetime import datetime, timedelta, date
import math
from sqlalchemy import desc, or_

from flask import Blueprint, flash, redirect, render_template, request, session
from flask_login import current_user, login_required, login_user

from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.resources import INLINE
from bokeh.models import LabelSet
from bokeh.models.annotations import Label

from app import db
from models import Activity, User
from activities.calculations import calculate_car_fuel, calculate_flight_distance, calculate_flight_emissions, calculate_motorbike_emissions, calculate_van_emissions, calculate_food_emissions, analyse_activity
from activities.forms import ActivityForm, ActivityDateForm, FuelForm, DistanceTravelledForm, FlightForm, CarSizeForm, MotorbikeSizeForm, VanSizeForm, FoodForm, FoodQuantityForm

activities_blueprint = Blueprint("activities", __name__, template_folder='templates')


@activities_blueprint.route('/activities/')
@login_required
def activities_home():
    return render_template("activities/home.html")


@activities_blueprint.route("/activities/resources")
@login_required
def activities_resources():
    return render_template("activities/resources.html")


@activities_blueprint.route("/activities/activity_analysis")
@login_required
def activity_analysis():
    time_frame = int(request.args.get("time_frame"))
    motor_activity = Activity.query.filter(Activity.user_id == current_user.id,
                                            or_(Activity.activity_type == "Car",
                                                Activity.activity_type == "Motorbike",
                                                Activity.activity_type == "Van"),
                                            Activity.date >= date.today() - timedelta(time_frame)).all()
    flight_activity = Activity.query.filter(Activity.user_id == current_user.id,
                                            Activity.activity_type == "Flight",
                                            Activity.date >= date.today() - timedelta(time_frame)).all()
    food_activity = Activity.query.filter(Activity.user_id == current_user.id,
                                          Activity.activity_type == "Food",
                                          Activity.date >= date.today() - timedelta(time_frame)).all()
    motor_emission = 0
    flight_emission = 0
    food_emission = 0
    for activity in motor_activity:
        motor_emission += activity.carbon_emission
    for activity in flight_activity:
        flight_emission += activity.carbon_emission
    for activity in food_activity:
        food_emission += activity.carbon_emission
    motor_result = analyse_activity("motor", motor_emission, time_frame)
    flight_result = analyse_activity("flight", flight_emission, time_frame)
    food_result = analyse_activity("food", food_emission, time_frame)
    return render_template("/activities/activity_analysis.html", motor_result=motor_result, flight_result=flight_result, food_result=food_result)


@activities_blueprint.route('/activities/add_activity', methods=["GET", "POST"])
@login_required
def add_activity():
    activity_form = ActivityForm()
    fuel_form = FuelForm()
    car_size_form = CarSizeForm()
    motorbike_size_form = MotorbikeSizeForm()
    flight_form = FlightForm()
    activity_date_form = ActivityDateForm()
    distance_travelled_form = DistanceTravelledForm()
    van_size_form = VanSizeForm()
    food_form = FoodForm()
    food_quantity_form = FoodQuantityForm()

    if request.method == "POST":

        # base form is present"Small"
        if request.form.get("activity") is not None:
            session["activity"] = activity_form.activity.data
            print(activity_form.activity.data)
            # if we chose car
            if activity_form.activity.data == "Car":
                # render the car fuel type
                return render_template("activities/add_activity.html",
                                    activity_form=activity_form,
                                    fuel_form=fuel_form,
                                    fade_in="fuel_form")

            # car chosen
            elif activity_form.activity.data == "Van":
                # render fuel type form
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       fuel_form=fuel_form,
                                       fade_in="fuel_form")

            # if we chose plane
            elif activity_form.activity.data == "Flight":
                # render the plane form
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       flight_form=flight_form,
                                       fade_in="flight_form")

            # if we chose motorbike
            elif activity_form.activity.data == "Motorbike":
                # render the motorbike form
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       motorbike_size_form=motorbike_size_form,
                                       fade_in="motorbike_size_form")

            # if we chose food
            elif activity_form.activity.data == "Food":
                # render food form
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       food_form=food_form,
                                       fade_in="food_form")


        # car -> fuel type
        if request.form.get("fuelType") is not None:
            session["fuel_type"] = fuel_form.fuelType.data
            if session["activity"] == "Car":
                # renders car size
                return render_template("activities/add_activity.html",
                                    activity_form=activity_form,
                                    fuel_form=fuel_form,
                                    car_size_form=car_size_form,
                                    fade_in="car_size_form")
            elif session["activity"] == "Van":
                # renders van size
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       fuel_form=fuel_form,
                                       van_size_form=van_size_form,
                                       fade_in="van_size_form")

        # car -> fuel type -> car size
        if request.form.get("carSize") is not None:
            session["car_size"] = car_size_form.carSize.data
            # renders distance travelled
            return render_template("activities/add_activity.html",
                            activity_form=activity_form,
                            fuel_form=fuel_form,
                            car_size_form=car_size_form,
                            distance_travelled_form=distance_travelled_form,
                            fade_in="distance_travelled_form")

        # motorbike -> motorbike size
        if request.form.get("motorbikeSize") is not None:
            session["motorbike_size"] = motorbike_size_form.motorbikeSize.data
            # render distance travelled
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   motorbike_size_form=motorbike_size_form,
                                   distance_travelled_form=distance_travelled_form,
                                   fade_in="distance_travelled_form")

        # van -> van size
        if request.form.get("vanSize") is not None:
            session["van_size"] = van_size_form.vanSize.data
            # render distance travelled
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   van_size_form=van_size_form,
                                   distance_travelled_form=distance_travelled_form,
                                   fade_in="distance_travelled_form")

        # car -> fuel type -> car size -> distance travelled
        # motorbike -> motorbike size -> distance travelled
        if request.form.get("distanceTravelled") is not None:
            session["distance_travelled"] = distance_travelled_form.distanceTravelled.data
            # renders activity date
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   fuel_form=fuel_form,
                                   car_size_form=car_size_form,
                                   distance_travelled_form=distance_travelled_form,
                                   activity_date_form=activity_date_form,
                                   fade_in="activity_date_form")

        # flight -> airports
        if request.form.get("startAirport") is not None:
            session["start_airport"] = flight_form.startAirport.data
            session["end_airport"] = flight_form.endAirport.data
            # renders activity date
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   flight_form=flight_form,
                                   activity_date_form=activity_date_form,
                                   fade_in="activity_date_form")

        # food -> select food
        if request.form.get("foodChoice") is not None:
            session["food_choice"] = food_form.foodChoice.data
            # renders food quantity form
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   food_form=food_form,
                                   food_quantity_form=food_quantity_form,
                                   fade_in="food_quantity_form")

        # food -> select food -> food quantity
        if request.form.get("foodQuantity") is not None:
            session["food_quantity"] = food_quantity_form.foodQuantity.data
            # renders activity date form
            return render_template("activities/add_activity.html",
                                   activity_form=activity_form,
                                   food_form=food_form,
                                   food_quantity_form=food_quantity_form,
                                   activity_date_form=activity_date_form,
                                   fade_in="activity_date_form")

        # food -> select food -> food quantity -> activity date
        # flight -> airports -> activity date
        # car -> fuel type -> car size -> distance travelled -> activity date
        # motorbike -> motorbike size -> distance travelled -> activity date
        if request.form.get("activityDate") is not None:
            if str(request.form.get("activityDate")) == "":
                flash("Please enter a vaid date.")
                return render_template("activities/add_activity.html",
                                       activity_form=activity_form,
                                       fade_in="activity_form")

            session["activity_date"] = activity_date_form.activityDate.data

            if current_user.is_authenticated:

                user_id = current_user.id
                if session["activity"] == "Car":
                    fuel = calculate_car_fuel(session["fuel_type"], session["fuel_type"], session["distance_travelled"])
                    activity = Activity(user_id, session["activity"], fuel, session["activity_date"], fuel_type=session["fuel_type"])

                elif session["activity"] == "Flight":
                    start_airport_code = session["start_airport"][-4:-1] # get the airport code
                    end_airport_code = session["end_airport"][-4:-1] # same <3

                    flight_distance = calculate_flight_distance(start_airport_code, end_airport_code) # in km
                    emissions = calculate_flight_emissions(flight_distance)

                    activity = Activity(user_id, session["activity"], emissions, session["activity_date"], flight_distance=flight_distance)

                elif session["activity"] == "Motorbike":
                    emissions = calculate_motorbike_emissions(session["distance_travelled"], session["motorbike_size"])
                    activity = Activity(user_id, session["activity"], emissions, session["activity_date"])

                elif session["activity"] == "Van":
                    emissions = calculate_van_emissions(session["van_size"], session["fuel_type"], session["distance_travelled"])
                    activity = Activity(user_id, session["activity"], emissions, session["activity_date"], fuel_type=session["fuel_type"])

                elif session["activity"] == "Food":
                    emissions = calculate_food_emissions(session["food_choice"], session["food_quantity"])
                    activity = Activity(user_id, session["activity"], emissions, session["activity_date"])


                db.session.add(activity)
                db.session.commit()

            flash("Your new activity has been added to your profile!")
            return redirect("/activities/")

    return render_template("activities/add_activity.html",
                           activity_form=activity_form,
                           fade_in="activity_form")


@activities_blueprint.route('/activities/activity_history')
@login_required
def activity_history():
    user_id = current_user.id
    
    match request.args.get("timeframe"):
        case "1d":
            time_from = datetime.now() - timedelta(days=1)
        case "7d":
            time_from = datetime.now() - timedelta(days=7)
        case "14d":
            time_from = datetime.now() - timedelta(days=14)
        case "1m":
            time_from = datetime.now() - timedelta(days=30)
        case "3m":
            time_from = datetime.now() - timedelta(days=90)
        case "6m":
            time_from = datetime.now() - timedelta(days=180)
        case "1y":
            time_from = datetime.now() - timedelta(days=365)
        case _:
            time_from = datetime.now() - timedelta(days=7)

    activities = Activity.query.filter(Activity.user_id == user_id, Activity.date >= time_from).order_by(desc(Activity.date))

    p = figure(
        height=350,
        sizing_mode="stretch_width",
        x_axis_type="datetime",
        x_axis_label="Activity Date",
        y_axis_label="Carbon Released (Kg)")

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    x_axis = []
    y_axis = []
    bar_labels = []

    total_footprint = 0
    for activity in activities:
        total_footprint = total_footprint + activity.carbon_emission
        activityDate = datetime(activity.date.year, activity.date.month, activity.date.day)
        carbon_emission = round(activity.carbon_emission)
        if len(x_axis) == 0:
            x_axis.append(activityDate)
            y_axis.append(carbon_emission)
            bar_labels.append(Label(x=activityDate, y=carbon_emission, text=str(carbon_emission), x_offset=-7.5, y_offset=5))
        else:
            activity_added = False
            for i in range(len(x_axis)):
                if x_axis[i] == activityDate:
                    y_axis[i] += carbon_emission
                    bar_labels[i].text = str(round(float(bar_labels[i].text), 2) + carbon_emission)
                    bar_labels[i].y = round(float(bar_labels[i].text), 2)
                    activity_added = True
                    break
            if not activity_added:
                x_axis.append(activityDate)
                y_axis.append(round(carbon_emission, 2))
                bar_labels.append(Label(x=activityDate, y=carbon_emission, text=str(carbon_emission), x_offset=-7.5, y_offset=5))
    
    for i in bar_labels:
        p.add_layout(i)
    p.vbar(
        x_axis,
        width=timedelta(0.25),
        bottom=0,
        top=y_axis,
        color="navy"
    )

    script, div = components(p)
    return render_template("activities/activity_history.html", activities_len=activities.count(), activities=activities, total_footprint=round(total_footprint, 2), div=div, script=script, js_resources=js_resources, css_resources=css_resources)
