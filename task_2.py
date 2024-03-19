import datetime

import dash
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

covid_data = pd.read_excel('covid_polymatica.xlsx')

regions = list(covid_data["Регион "].unique())
city_options = [{'label': region, 'value': region} for region in regions]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Статистика COVID-19 в регионах России")
    ], className="header-box"),

    dcc.Dropdown(
        id='region-dropdown',
        options=city_options,
        value='Москва'
    ),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=covid_data.iloc[:, 2].min(),
        end_date=covid_data.iloc[:, 2].max(),
        display_format='YYYY-MM-DD'
    ),

    dcc.Graph(id='diseases-graph'),
    dcc.Graph(id='deaths-graph')
])


@app.callback(
    [
        Output('diseases-graph', 'figure'),
        Output('deaths-graph', 'figure')
    ],
    [
        Input('region-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def update_graphs(selected_region, start_date, end_date):
    print(selected_region)
    print(np.datetime64(start_date))
    print(np.datetime64(end_date))





    filtered_data = covid_data[(covid_data.iloc[:, 0].isin(selected_region)) &
                               (covid_data.iloc[:, 2] >= start_date) &
                               (covid_data.iloc[:, 2] <= end_date)]

    cases_figure = px.line(filtered_data, x=covid_data.columns[2], y=covid_data.columns[3],
                           color=covid_data.columns[0],
                           title='Количество заболевших по регионам')

    deaths_figure = px.line(filtered_data, x=covid_data.columns[2], y=covid_data.columns[5],
                            color=covid_data.columns[0],
                            title='Количество смертей по регионам')

    return cases_figure, deaths_figure


if __name__ == '__main__':
    app.run_server(debug=True)
