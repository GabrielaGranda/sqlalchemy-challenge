# Import the dependencies.
from flask import Flask, jsonify

from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)
print(f"{Base.classes.keys()}")
# Save references to each table

Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    return (f"Welcome to my page: Climate App<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).all()
    pre_dic = dict(query_data)

    session.close()

    return jsonify(pre_dic)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    list_stations = session.query(Station.station, Station.name).all()
    station_dic = list(np.ravel(list_stations))

    session.close()

    return jsonify(station_dic)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    list_tobs = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').all()

    session.close()

    all_tobs = []
    for tobs, date in list_tobs:
        tobs_dict = {}
        tobs_dict["tobs"] = tobs
        tobs_dict["date"] = date
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_end_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    return_data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    all_start = []
    for min_tobs, max_tobs, avg_tobs in return_data:
        tobs_temp_dict = {}
        tobs_temp_dict["Min Temp"] = min_tobs
        tobs_temp_dict["Max Temp"] = max_tobs
        tobs_temp_dict["Avg Temp"] = avg_tobs
        all_start.append(tobs_temp_dict)

    session.close()
    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    return_data_stend = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    all_start_end = []
    for min_tobs, max_tobs, avg_tobs in return_data_stend:
        tobs_stend_dict = {}
        tobs_stend_dict["Min Temp"] = min_tobs
        tobs_stend_dict["Max Temp"] = max_tobs
        tobs_stend_dict["Avg Temp"] = avg_tobs
        all_start_end.append(tobs_stend_dict)

    session.close()
    return jsonify(all_start_end)

if __name__ == "__main__":
    app.run(debug=True)