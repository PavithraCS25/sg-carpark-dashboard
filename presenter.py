#!/usr/bin/env python
# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import dash_bootstrap_components as dbc
import processor as pr

'''
Created by: Pavithra Coimbatore Sainath
Date: 15th Apr 2021

'''

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = False

# Generating Layout of the Dashboard
app.layout = html.Div(
    [
        html.H3("SG Car Park Utilization Study", style={"textAlign": "center", "margin": "2px", "padding": "2px", "width": "100%", "color":"white", "background-color": "#007bff" }),
        html.Br(),
        html.H5("Select Dates"),
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=date(2018, 2, 13),
            max_date_allowed=date(2018, 2, 23),
            start_date=date(2018, 2, 13),
            end_date=date(2018, 2, 14),
        ),
        html.Br(),
        html.Br(),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Car Park Metrics",
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H5("Most Underutilized Car Park"),
                                        html.Span(
                                            "Question 1", className="btn btn-primary"
                                        ),
                                        dcc.Loading(
                                            id="loading-2",
                                            type="circle",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="Most_Underutilized_Car_Park"
                                                        )
                                                    ]
                                                )
                                            ],
                                        ),
                                    ],
                                    style={
                                        "height": "50%",
                                        "width": "50%",
                                        "float": "left",
                                    },
                                ),
                                html.Div(
                                    children=[
                                        html.H5("Largest Car Park"),
                                        html.Span(
                                            "Question 2", className="btn btn-primary"
                                        ),
                                        dcc.Loading(
                                            id="loading-1",
                                            type="circle",
                                            children=[
                                                html.Div(
                                                    [dcc.Graph(id="largest_car_park")]
                                                )
                                            ],
                                        ),
                                    ],
                                    style={
                                        "height": "50%",
                                        "width": "50%",
                                        "float": "left",
                                    },
                                ),
                                html.Div(
                                    children=[
                                        html.H5("Most Underutilized Car Park"),
                                        dcc.Loading(
                                            id="loading-3",
                                            type="circle",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="Most_Underutilized_Car_Park_2"
                                                        )
                                                    ]
                                                )
                                            ],
                                        ),
                                    ],
                                    style={
                                        "height": "50%",
                                        "width": "50%",
                                        "float": "left",
                                    },
                                ),
                                html.Div(
                                    children=[
                                        html.H5("Car Park Utilization Trend"),
                                        dcc.Loading(
                                            id="loading-4",
                                            type="circle",
                                            children=[
                                                html.Div(
                                                    [dcc.Graph(id="Utilization_Trend")]
                                                )
                                            ],
                                        ),
                                    ],
                                    style={
                                        "height": "50%",
                                        "width": "50%",
                                        "float": "left",
                                    },
                                ),
                            ],
                            style={"height": "100%", "margin": "0", "padding": "0", "border": "1px"},
                        )
                    ],
                ),
                dcc.Tab(
                    label="Lot Type based Occupancy",
                    children=[
                        html.Div(
                            children=[
                                html.H5("Lot Type Occupancy by Frequency"),
                                dcc.Loading(
                                    id="loading-5",
                                    type="circle",
                                    children=[
                                        html.Div(
                                            children=[
                                                dcc.Graph(id="Utilization_by_Lot_Type")
                                            ],
                                            style={
                                                "height": "50%",
                                                "width": "50%",
                                                "float": "left",
                                            },
                                        )
                                    ],
                                ),
                                html.H5("Lot Type Occupancy by Frequency and Car Park Type"),
                                dcc.Loading(
                                    id="loading-6",
                                    type="circle",
                                    children=[
                                        html.Div(
                                            children=[
                                                dcc.Graph(id="Utilization_by_lt_cp")
                                            ],
                                            style={
                                                "height": "50%",
                                                "width": "50%",
                                                "float": "right",
                                            },
                                        )
                                    ],
                                ),
                            ],
                            style={"height": "100%", "margin": "0", "padding": "0", "border": "1px"},
                        )
                    ],
                ),
                dcc.Tab(
                    label="Car Park Utilization by Area",
                    children=[
                        html.Div(
                            children=[
                                html.H5("Car Park Utilization by area"),
                                html.Img(
                                    src=app.get_asset_url("car_park_choropleth.png"),
                                    style={"height": "100%", "width": "100%"},
                                ),
                            ]
                        )
                    ],
                ),
                dcc.Tab(
                    label="Data Set Samples",
                    children=[
                        html.Div(children=[html.H5("Data Overview"), pr.generate_table()])
                    ],
                ),
            ]
        ),
    ]
)


@app.callback(
    [dash.dependencies.Output('largest_car_park', 'figure'),
     dash.dependencies.Output('Most_Underutilized_Car_Park', 'figure'),
     dash.dependencies.Output('Most_Underutilized_Car_Park_2', 'figure'),
     dash.dependencies.Output('Utilization_Trend', 'figure'),
     dash.dependencies.Output('Utilization_by_Lot_Type', 'figure'),
     dash.dependencies.Output('Utilization_by_lt_cp', 'figure')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    start_date_string = ""
    end_date_string = ""
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
    merged_data = pr.prepare_data(start_date_string, end_date_string)
    fig0 = pr.largest_carpark(merged_data)
    fig1 = pr.most_underutilized_car_park(merged_data)
    fig2 = pr.most_underutilized_car_park_occupancy(merged_data)
    fig3 = pr.most_utilized_lt(merged_data)
    fig4 = pr.most_utilized_cp_lt(merged_data)
    fig5 = pr.utilization_trend(merged_data)
    return [fig0, fig1, fig2, fig5, fig3, fig4]


# Main


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
