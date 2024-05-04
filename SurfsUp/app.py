# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')

import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

from flask import Flask, jsonify

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/startdate<br/>"
        f"/api/v1.0/temp/start/startdate/end/enddate<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>")

#Retrieve precipitation values from the last year of data and put results in a dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():


    most_recent_date = (session.query(measurement.date).order_by(measurement.date.desc()).first()[0])
    year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=366)


    data = [measurement.date, measurement.prcp]
    precipitation_scores = session.query(*data).filter(measurement.date >= year_ago).all()


    precipitation_pastyear = []
    for date, prcp in precipitation_scores:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_pastyear.append(precipitation_dict)
  
    return jsonify(precipitation_pastyear)

#Retrieve stations from the dataset and put into a list
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()

    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

#Retrieve temperatures from the last year for the most-active station
@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = (session.query(measurement.date).order_by(measurement.date.desc()).first()[0])
    year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=366)

    temperature_data = session.query(measurement.tobs).\
        filter(measurement.date >= year_ago).\
        filter(measurement.station == "USC00519281").all()
    
    temperature = list(np.ravel(temperature_data))

    return jsonify(temperature)

#Create function to retrieve min, average and max temperatures for specific start and end dates
def startend(start, end=None):
    
    start_date = dt.datetime.strptime(start, "%m%d%Y")

    if end is None:
        most_recent_date = (session.query(measurement.date).order_by(measurement.date.desc()).first()[0])
        end_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    else:
        end_date = dt.datetime.strptime(end, "%m%d%Y")

    data = func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)

    results= session.query(*data).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()
    
    startendlist = list(np.ravel(results))

    return jsonify(startendlist)

#Retrieve min, average and max temperatures for a specific start and end date
@app.route("/api/v1.0/temp/start/<start>/end/<end>")
def startend_with_end(start, end):
    return startend(start, end)   

#Retrieve min, average and max temperatures for a specific start date and no end date provided
@app.route("/api/v1.0/temp/start/<start>")
def startend_no_end(start):
    return startend(start)    

if __name__ == "__main__":
    app.run(debug=True)

session.close()