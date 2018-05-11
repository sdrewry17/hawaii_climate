#dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta

#defining teh app
app = Flask(__name__)

#Turn all the data into JSON
measurement_path = ('c:/Users/sethd/OneDrive/Documents/GWU Data Analytics/SQL_with_python/sql_python_homework/clean_hawaii_measurements.csv')
measurement_df = pd.read_csv(measurement_path)
measurement_df_TTM = measurement_df[measurement_df['date'] > "2016-08-23"]
max_date = measurement_df['date'].max()
min_date = measurement_df['date'].min()

temp_params = ['tmin', 'tmax', 'tavg']

#NOTE - NEED TO CONVERT THE DATES TO THE RIGHT FORMAT BEFORE TURNING INTO A JSON

station_path = ('c:/Users/sethd/OneDrive/Documents/GWU Data Analytics/SQL_with_python/sql_python_homework/clean_hawaii_stations.csv')
station_df = pd.read_csv(station_path)

#defining the routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For the following routes, dates must be in YYYY-MM-DD format and be between 2010-01-01 and 2017-08-23:<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    '''Query for the dates and temperature observations from the last year.
    Convert the query results to a Dictionary using date as the key and tobs as the value.
    Return the json representation of your dictionary.'''

    measurement_df_TTM.drop(['station', 'tobs'], axis = 1, inplace = True)
    precip_json = measurement_df_TTM.to_json(orient = 'records')

    return precip_json
        

@app.route("/api/v1.0/stations")
def stations():
    '''Return a json list of stations from the dataset'''
    
    station_json = station_df.to_json(orient = 'records')
    
    return station_json


@app.route("/api/v1.0/tobs")
def tobs():
    '''Return a json list of Temperature Observations (tobs) for the previous year'''

    measurement_df_TTM.drop(['station', 'prcp'], axis = 1, inplace = True)
    tobs_json = measurement_df_TTM.to_json(orient = 'records')

    return tobs_json


@app.route("/api/v1.0/<start>")
def start_date(start):
    '''Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.'''
    
    start_measurement_df = measurement_df[measurement_df['date'] > start]
    tobs_series = start_measurement_df['tobs']
    tmin = tobs_series.min()
    tmax = tobs_series.max()
    tavg = tobs_series.mean()

    temp_dict = {"tmin": tmin, 'tmax': tmax, 'tavg': tavg}
    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_to_end_date(start, end):
    '''When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.'''

    start_end_measurement_df = measurement_df[(measurement_df['date'] > start) & (measurement_df['date'] < end)]
    tobs_series = start_end_measurement_df['tobs']
    
    tmin = tobs_series.min()
    tmax = tobs_series.max()
    tavg = tobs_series.mean()

    temp_dict = {"tmin": tmin, 'tmax': tmax, 'tavg': tavg}
    return jsonify(temp_dict)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)



