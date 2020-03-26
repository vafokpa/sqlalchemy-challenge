import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from collections import defaultdict 
import datetime as dt
import datetime as datetime

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# . Create an app, being sure to pass __name__
app = Flask(__name__)





# 1 Available Routes

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return '''Welcome to my app! 
           <br /> Available Routes: 
           <br /> 1) /api/v1.0/precipitation
           <br /> 2) /api/v1.0/stations
           <br /> 3) /api/v1.0/tobs
           <br /> 4) /api/v1.0/<start> 
           <br /> 5) /api/v1.0/<start>/<end>'''


# 2 Precipitation Data

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Query of date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    # Convert list of Tuples into a dictionary

    precip_data = defaultdict(list) 
    for i, j in results: 
        precip_data[i].append(j) 

    return jsonify(precip_data)

# 3 Stations Data
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Query for stations
    results2 = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results2))

    return jsonify(all_stations)

# 4 Temperature Observations Data
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Query to find date a year ago
   # Latest Date
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # date 12 months ago from last entry
    year_ago= datetime.datetime.strptime(last_date[0], '%Y-%m-%d').date() - dt.timedelta(days=366)


   # Query of date and tobs a year from the previous year
    results3 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > str(year_ago)).\
        order_by(Measurement.date).all()

    session.close()

    # Convert list of Tuples into singular list
    tobs_list = [x[1] for x in results3]

    return jsonify(tobs_list)


 # 5 Start Stats when they give us a start date
@app.route("/api/v1.0/<start>")
def start(start):


    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for temperature data on the date given
    # Lowest Temperature
    tmin = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date > start).first()

    # Highest Temperature
    tmax = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date > start).first()

    # Average Temperature
    tavg = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date > start).first()

    session.close()

    return jsonify([tmin[0],tavg[0],tmax[0]])


 # 5 Start and End - when they give us a start date and end date
@app.route("/api/v1.0/<start>/<end>")
def end(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for temperature data on the date given
    # Lowest Temperature
    tmin1 = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date > start).\
    filter(Measurement.date < end).first()

    # Highest Temperature
    tmax1 = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date > start).\
    filter(Measurement.date < end).first()

    # Average Temperature
    tavg1 = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date > start).\
    filter(Measurement.date < end).first()

    session.close()

    return jsonify([tmin1[0],tavg1[0],tmax1[0]])

if __name__ == "__main__":
    app.run(debug=True)
