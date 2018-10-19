import os

from flask import Flask, render_template, request
from orm import *
from flask import jsonify

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""
    
    #Get form information.
    name = request.form.get("name")
    if name == "":
        return render_template("error.html", message="Cannot create a passenger without a name.")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Wrong flight number.")
    
    #Make sure the flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No such flight with that id.")
    passenger=Passenger(name=name, flight_id=flight_id)
    db.session.add(passenger)
    db.session.commit()
    
    return render_template("success.html", flight_id=flight_id)

@app.route("/flights/<int:flight_id>", methods=["GET"])
def flight(flight_id):
    """Passengers"""
    
    #Listing passengers for a specific flight
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No such flight.")
    
    passengers = Passenger.query.filter_by(flight_id=flight_id).all()
    if passengers is None:
        return render_template("error.html", message="No passengers for this flight")
    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    """Return details about a flight"""
    
    # Make sure a flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({
            "success": False,
            "error": "Invalid flight number"
        }), 422
    
    # Get all passengers
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
        "success": True,
        "origin": flight.origin,
        "destination": flight.destination,
        "duration": flight.duration,
        "passengers": names
    })

@app.route("/api/flights")
def flights_api():
    """Returns list of all flights"""
    
    flights = Flight.query.all()
    flightsList=[]
    for flight in flights:
        flightsList.append({"id": flight.id, "origin": flight.origin, "destination": flight.destination, "duration": flight.duration})
    return jsonify({
        "flights": flightsList
    })
        