# Import the dependencies.

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

from flask import Flask,jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017<br/>"
        f"/api/v1.0/spring_2017"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp)

    session.close()

    prcp_results = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_results.append(prcp_dict)
    return jsonify(prcp_results)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name,Station.latitude,
                            Station.longitude, Station.elevation).all()

    session.close()

    station_results = []
    for station,name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_results.append(station_dict)

    

    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    sel = [Measurement.station,
        Measurement.date,
        Measurement.tobs]
    
    results = session.query(*sel).\
        filter(Measurement.date <= dt.date(2017, 8, 18)).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.desc()).all()    
    
    session.close()

    tobs_results = []
    for station,date,tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_results.append(tobs_dict)

    return jsonify(tobs_results)

@app.route("/api/v1.0/2017")
def last_year():
    session = Session(engine)
    data_2017 = dt.date(2017, 1, 1)
    TMAX = func.max(Measurement.tobs)
    TMIN = func.min(Measurement.tobs)
    TAVG = func.avg(Measurement.tobs)
    
    results = session.query(TMAX,\
    TMIN,\
    TAVG).\
    filter(Measurement.date >= data_2017).all()

    session.close()

    year_2017 =[]
    for TMAX,TMIN,TAVG in results:
        dict_2017= {}
        dict_2017["2017 Max Temp"] = TMAX
        dict_2017["2017 Min Temp"] = TMIN
        dict_2017["2017 Average Temp"] = TAVG
        year_2017.append(dict_2017)
    

    return jsonify(year_2017)

@app.route("/api/v1.0/spring_2017")
def start_end():
    session = Session(engine)
    spring_equinox = dt.date(2017, 3, 20)
    summer_solstice = dt.date(2017, 6, 20)
    TMAX = func.max(Measurement.tobs)
    TMIN = func.min(Measurement.tobs)
    TAVG = func.avg(Measurement.tobs)
    
    results = session.query(TMAX,\
    TMIN,\
    TAVG).\
    filter(Measurement.date >= spring_equinox).\
    filter(Measurement.date <= summer_solstice)    
    session.close()

    spring_2017 =[]
    for TMAX,TMIN,TAVG in results:
        spring_dict= {}
        spring_dict["Spring 2017 Max Temp"] = TMAX
        spring_dict["Spring 2017 Min Temp"] = TMIN
        spring_dict["Spring 2017 Average Temp"] = TAVG
        spring_2017.append(spring_dict)

    return jsonify(spring_2017)

if __name__ == '__main__':
    app.run(debug=True) 