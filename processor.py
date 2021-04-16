#!/usr/bin/env python
# coding: utf-8

import sqlite3

import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px

'''
Created by: Pavithra Coimbatore Sainath
Date: 15th Apr 2021

'''

# Sample dates for generating the data table
DATA_GEN_START_DATE = "2018-02-13"
DATA_GEN_END_DATE = "2018-02-14"

'''
This function returns the data from sqlite Database. 
Sqlite Database will be populated by DataImport.py through API scrapping.
'''


def get_data(start_date, end_date):
    try:
        db = sqlite3.connect('./data/Carpark_15min')
        car_park_avail_data = pd.read_sql_query(
            "SELECT * from carpark_availability_15min where timestamp between ? and ?", db,
            params=(start_date, end_date))

        # Read carpark reference data from a csv file
        carpark_ref_data = pd.read_csv('./data/hdb-carpark-information/hdb-carpark-information.csv')
        return car_park_avail_data, carpark_ref_data
    except Exception as E:
        print('Error: ', E)
    else:
        db.close()


'''
To display . 
Sqlite Database will be populated by DataImport.py through API scrapping.
'''


def convert_million_to_thousands(values):
    return [str(num / 1000) + 'k' for num in values]


'''
1. Filter data with 'Electronic car park system' and 'Whole day parking' as per business needs.
2. Merge the car park availability data with car park reference data.
3. Remove null values and do basic preprocessing

'''


def prepare_data(start_date, end_date):
    carpark_availability_data, carpark_ref_data = get_data(start_date, end_date)
    carpark_availability_data['total_lots'] = carpark_availability_data['total_lots'].astype(int)
    carpark_availability_data['lots_available'] = carpark_availability_data['lots_available'].astype(int)

    # eliminate the records with total lots 0, as it is not meaningful to have total lots value 0
    carpark_availability_data = carpark_availability_data[carpark_availability_data['total_lots'] > 0]

    # Available lots cannot be greater than total lots, hence remove those records
    carpark_availability_data = carpark_availability_data[
        carpark_availability_data['lots_available'] < carpark_availability_data['total_lots']]
    carpark_availability_data['carpark_number'] = carpark_availability_data['carpark_number'].str.strip()
    carpark_ref_data['car_park_no'] = carpark_ref_data['car_park_no'].str.strip()

    # Data filtered based on business model
    carpark_ref_data = carpark_ref_data[(carpark_ref_data['short_term_parking'] == 'WHOLE DAY') & (
                carpark_ref_data['type_of_parking_system'] == 'ELECTRONIC PARKING')]

    # join two tables based on car park number column
    merged_data = pd.merge(left=carpark_ref_data, right=carpark_availability_data, how='left', left_on='car_park_no',
                           right_on='carpark_number')

    # Total lots cannot be null for a carpark, remove null values
    merged_data = merged_data[merged_data['total_lots'].notnull()]
    merged_data['total_lots'] = merged_data['total_lots'].astype('int')
    merged_data['%occupied'] = 1 - (merged_data['lots_available'] / merged_data['total_lots'])
    merged_data.car_park_decks = merged_data.car_park_decks.apply(str)
    return merged_data


'''
Question 2: Find the Largest Car Park
Plot in bar graph
'''


def largest_carpark(merged_data):
    # Largest carpark data
    largest_cp_data = merged_data.groupby(['timestamp']).apply(lambda x: x.nlargest(5, 'total_lots')).reset_index(
        drop=True)
    total_lot_data = largest_cp_data.groupby('car_park_no').mean()
    total_lot_data = total_lot_data.reset_index()
    total_lot_data = total_lot_data.sort_values('total_lots', ascending=False)
    fig = px.bar(total_lot_data, x="car_park_no", y="total_lots", color="total_lots", color_continuous_scale='Blues')
    fig.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Car Park Number", yaxis_title="Total Lots")
    fig.update_traces(marker_line_width=0)
    return fig


'''
Question 1: Find the Most underutilized car park
Plot in bar graph
'''


def most_underutilized_car_park(merged_data):
    occ_data = merged_data.groupby(['timestamp']).apply(lambda x: x.nsmallest(5, '%occupied')).reset_index(drop=True)
    cp_count = occ_data['car_park_no'].value_counts()
    cp_count = cp_count[:10, ]
    fig_1 = px.bar(cp_count, x=cp_count.index, y=cp_count.values,color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_1.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Car Park Number", yaxis_title="%occupied")
    fig_1.update_traces(marker_line_width=0)
    return fig_1


'''
Question 1: Find the Most underutilized car park by Occupancy
Plot in bar graph
'''


def most_underutilized_car_park_occupancy(merged_data):
    occ_data = merged_data.groupby(['timestamp']).apply(lambda x: x.nsmallest(5, '%occupied')).reset_index(drop=True)
    filter_v = dict(occ_data['car_park_no'].value_counts().nlargest(10))
    under_ut_data = occ_data[occ_data['car_park_no'].isin(list(filter_v.keys()))]
    under_ut_data['counts'] = under_ut_data['car_park_no'].map(under_ut_data['car_park_no'].value_counts())
    under_ut_data = under_ut_data.groupby(['car_park_no']).mean()
    under_ut_data = under_ut_data.sort_values('%occupied', ascending=False)

    fig_2 = px.bar(under_ut_data, x=under_ut_data.index, y=under_ut_data['%occupied'], color="counts",
                   color_continuous_scale='Blues')
    fig_2.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Car Park Number", yaxis_title="%occupied")
    fig_2.update_traces(marker_line_width=0)
    return fig_2


'''
Find the most frequently used car park Lot Type  by Occupancy
Plot in bar graph
'''


def most_utilized_lt(merged_data):
    # Most utilized lot type and car park type
    merged_data['counts'] = merged_data['lot_type'].map(merged_data['lot_type'].value_counts())
    ut_data = merged_data.groupby('lot_type').mean()
    ut_data = ut_data.sort_values('%occupied', ascending=False)
    fig_3 = px.bar(ut_data, x=ut_data.index, y='%occupied', color="counts", color_continuous_scale='Blues')
    fig_3.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Lot Type")
    fig_3.update_traces(marker_line_width=0)
    return fig_3


'''
Find the most occupied used car park Lot Type for each car park type
Plot in grouped bar graph
'''


def most_utilized_cp_lt(merged_data):
    # Most utilized lot type and car park type
    merged_data['counts'] = merged_data['lot_type'].map(merged_data['lot_type'].value_counts())
    ut_cp_data = merged_data.groupby(['lot_type', 'car_park_type']).mean()
    ut_cp_data = ut_cp_data.reset_index()
    ut_cp_data = ut_cp_data.sort_values('%occupied', ascending=False)
    fig_4 = px.bar(ut_cp_data, x='car_park_type', y='%occupied', color='lot_type', barmode="group",
                   color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_4.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Car Park Type")
    fig_4.update_traces(marker_line_width=0)
    return fig_4


'''
To explore the utilization trend of the car park availability data with 30 minute window
Plot in line graph
'''


def utilization_trend(merged_data):
    # Utilization trend 30 minute window
    t_data = merged_data.copy()
    t_data.index = pd.to_datetime(t_data.timestamp)
    t_data = t_data["%occupied"].resample("30T").apply([np.mean])
    fig_5 = px.line(t_data, x=t_data.index, y="mean", title="Utilization Trend - 30 minute window",color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_5.update_layout(plot_bgcolor="#FFFFFF", xaxis_title="Date", yaxis_title="Mean Occupancy")
    return fig_5


'''
Fetch the data for overview
Plot in a Table
'''


def generate_table(max_rows=100):
    dataframe = prepare_data(DATA_GEN_START_DATE, DATA_GEN_END_DATE)
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'border': '1px', "width": "100%", "overflow": "scroll"})