import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Base.classes.keys()

#Save reference to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/stats/<start><br/>"
    f"/api/v1.0/range/<start>/<end>/")

#Route one
#Get precipitation data from last year of data set
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
            
    measurements = session.query(Measurement).filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23')
    
    print([x for x in measurements])
    # return[x for x in measurements]
    
    precip_dict = {}
    for measurement in measurements:
        precip_dict[measurement.date] = measurement.prcp

    session.close()
    return jsonify(precip_dict)

#Route two
#Get list of unique stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    unique_stations = session.query(Measurement.station).group_by("station").all()
    print(type(unique_stations))
    print(unique_stations)
    
    results = []
    for station in unique_stations:
        results.append(station[0])
    print(results)
    
    session.close()
    return jsonify(results)

#Route three
#Get temperatures from most active station from the last year of data set
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    active_station = session.query(Measurement).filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == "USC00519281").all()
        
    station_data = {}
    for data in active_station:
        station_data[data.date] = data.tobs

    session.close()
    return jsonify(station_data)

#Route four
#Find min, max, and avg temperatures from most active station on a specific date
@app.route("/api/v1.0/stats/<start>")
def stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print(start)
    
    min_temp =  session.query(func.min(Measurement.tobs)).filter_by(station="USC00519281").\
         filter(Measurement.date >= start).all()

    max_temp =  session.query(func.max(Measurement.tobs)).filter_by(station="USC00519281").\
         filter(Measurement.date >= start).all()

    avg_temp =  session.query(func.avg(Measurement.tobs)).filter_by(station="USC00519281").\
         filter(Measurement.date >= start).all()

    station_stats = [min_temp, max_temp, avg_temp]
    station_stats = list(np.ravel(station_stats))
    return jsonify(station_stats)

#Route five
#Find min, max, and avg temperatures from most active station within a date range
@app.route("/api/v1.0/range/<start>/<end>/")
def range(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print(start, end)
    
    min_tem =  session.query(func.min(Measurement.tobs)).filter_by(station="USC00519281").\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
         
    max_tem =  session.query(func.max(Measurement.tobs)).filter_by(station="USC00519281").\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    avg_tem =  session.query(func.avg(Measurement.tobs)).filter_by(station="USC00519281").\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    station_range = [min_tem, max_tem, avg_tem]
    station_range = list(np.ravel(station_range))
    return jsonify(station_range)

#Run
if __name__ == "__main__":
    app.run(port = 5001, debug=True)

