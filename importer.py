#!/usr/bin/env python
# coding: utf-8
import requests
import pandas as pd
from time import sleep
from datetime import datetime
import sqlite3

'''
Created by: Pavithra Coimbatore Sainath
Date: 15th Apr 2021

'''

'''
This function returns the date range for the given start and end dates
This will be used to generate the list of timestamps for the given dates
'''

CAR_PARK_URL = 'https://api.data.gov.sg/v1/transport/carpark-availability'


def get_date_range(start_date, end_date):
    datelist = [str(i).replace(' ', 'T') for i in pd.date_range(start=start_date, end=end_date, freq="15min")]
    return datelist


'''
This function returns the json response for the given url with its parameters
'''


def get_response(url, param, timeout=60):
    response = requests.get(url, params=param)
    if response.status_code != 200:
        sleep(10)
        return get_response(url, param)
    else:
        res_json = response.json()
        return res_json


'''
This function normalizes the data and transforms the data into a dataframe format
'''


def normalize(timestamp, response):
    for t in response['items']:
        df = pd.DataFrame.from_dict(
            pd.json_normalize(t['carpark_data'], 'carpark_info', ['carpark_number', 'update_datetime']))
        df['timestamp'] = timestamp
        return df


'''
This function used to create database table and insert the data to the database
The table is created only if is not already available
'''


def write_to_db(dataframe):
    if not dataframe is None:
        try:
            db = sqlite3.connect('Carpark_15min')
            cursor = db.cursor()
            cursor.execute('''create table if not exists carpark_availability_15min (total_lots varchar(20),lot_type varchar(5),
                        lots_available varchar(10),carpark_number varchar(20),update_datetime datetime,timestamp datetime, PRIMARY KEY (carpark_number,lot_type,timestamp))''')

        except Exception as E:
            print('Error :', E)
        else:
            print('table created or updated')

        try:
            dataframe.to_sql(name='carpark_availability_15min', con=db, if_exists='append', index=False)
        except Exception as E:
            print('Error : ', E)
            db.commit()
            print('data inserted')
    else:
        print('Empty DF')


'''
Configured 60 seconds sleep as throttling in the api.data.gov.sg imposes rate limiting
'''

if __name__ == "__main__":
    start_dt = input('Enter start date').replace('/', '-')
    end_dt = input('Enter end date').replace('/', '-')

    if datetime.strptime(start_dt, '%Y-%m-%d') > datetime.strptime(end_dt, '%Y-%m-%d'):
        print('Please enter a valid start and end date. End date should be larger than the start date.')
    else:
        date_list = get_date_range(start_dt, end_dt)
        for date in date_list:
            PARAM = {'date_time': date}
            response_data = get_response(CAR_PARK_URL, PARAM)
            write_to_db(normalize(date, response_data))
            sleep(60)
