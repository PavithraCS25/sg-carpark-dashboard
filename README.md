# Singapore Car park data analytics

## Importer 
- Source : https://data.gov.sg/dataset/carpark-availability
- Downloads Singapore Car park data from API hosted at https://api.data.gov.sg/v1/transport/carpark-availability
- Data from 2018-02-13 to 2018-02-23 with 15 minute interval is fetched and stored in the SQLite database
- The source site is throttled and rate limited to 60 minutes/minute for fetching the data
- SQLite DB stores around 1.6 Million records as result of scraping job (importer.py)

### SQLite Table Structure

| Column | Description |
| --- | --- |
| total_lots | Total car park lots in the car park number|
| lot_type | Lot type of car park [C, Y, H] |
| lots_available | Car park lots available in the car park number |
| carpark_number | Car Park number is the unique identifier indicating the car park |
| update_datetime | Timestamp last updated data |
| timestamp | Timestamp interval on which API data is fetched |

## Pre-Requisite 

SQLite file: https://drive.google.com/file/d/1FEVOPH231oVRXnfOVlyykoqcW0JVRvd3/view?usp=sharing
Copy Location: ./data/

## Processor

- Null values removal on all data columns received from the API
- Conversion of String columns to Integer for total lots
- Striping and cleaning of data points
- Calculation of percentage occupied 1- (LOTS_AVAILABLE / TOTAL_LOTS)
- Plot creation logic implementation

## presenter 

- Presenter will launch the dashboard for presenting the analysis 
- Uses processor for the plot implementation which executes car park data transformation and car park data pre-processing executions


| Plot Category | Plot Type |
| --- | --- |
| Car park metrics | Most Underutilized Car Park |
| Car park metrics | Largest Car Park |
| Car park metrics | Most Underutilized Car Park |
| Car park metrics | Car Park Utilization Trend |
| Lot Type based Occupancy | Lot Type Occupancy by Frequency |
| Lot Type based Occupancy | Lot Type Occupancy by Frequency and Car Park Type |
| Car Park Utilization by Area | Overall data plotted on Choropleth map image |
| Data set samples | Sample data overview |

## Technical Stack

- Python 3.8
- Python Dash
- SQLite
- Plotly


## Run Steps

- Open Terminal
- [execute] python presenter.py 
    - click on the server link (Ex: http://127.0.0.1:8050/)


