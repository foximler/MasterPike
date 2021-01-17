from flask import Blueprint, render_template, request, jsonify
from . import db
from flask_login import login_required, current_user
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from datetime import datetime
import pandas as pd
from database import create_database, update_database, getstatus
from message import send_message, claim_rig
main = Blueprint('main', __name__)
@main.route('/api')
def api_uuid():
    # Check if a UUID was provided as part of the URL
    # If UUID is provided, assign it to a variable
    # If not UUID is provided, display error in browser
    # Repeat for other arguments
    arguments = ['uuid', 'temp', 'humid', 'alert', 'lat', 'long', 'time']
    argument_data = {}
    for argument in arguments:
        if argument in request.args:
            if request.args[argument] is not None:
                argument_data[argument] = request.args[argument]
        else:
            return f"Error, {argument} not provided. Please specify a {argument}"

    update_database(argument_data)
    if argument_data['alert'] == 1:
        send_message('content.txt', argument_data['uuid'])

    return "Successful request!"
@main.route('/claimrig')
def api_claim():
    # Check if a UUID was provided as part of the URL
    # If UUID is provided, assign it to a variable
    # If not UUID is provided, display error in browser
    # Repeat for other arguments
    arguments = ['uuid']
    argument_data = {}
    for argument in arguments:
        if argument in request.args:
            if request.args[argument] is not None:
                argument_data[argument] = request.args[argument]
        else:
            return f"Error, {argument} not provided. Please specify a {argument}"

    claim_rig(current_user.notification,argument_data)
    currentstatus = getstatus(str(current_user.notification))
    return render_template('profile.html', name = current_user.name, items=currentstatus, email= current_user.notification)

@main.route('/')
def index():
    return render_template('index.html')
@main.route('/monitor')
@login_required
def profile():
    #while it is dangerous to give all data back to the user our databases are seperated and  this is likely a private client for now. 
    currentstatus = getstatus(str(current_user.notification))
    return render_template('profile.html', name=current_user.name, items=currentstatus,email=current_user.notification)


