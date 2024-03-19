import dash
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

covid_data = pd.read_excel('covid_polymatica.xlsx')
covid_data = covid_data[["Регион ", "дата", "случаи заболевания", "количество смертей"]]

regions = list(covid_data["Регион "].unique())
city_options = [{'label': region, 'value': region} for region in regions]

external_stylesheets = ['/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Lab 3, task 2'

app.layout = html.Div([
    html.Div([
        html.H1("Covid 19 data by region in Russia:")
    ], className="header-box"),

    html.Div([
        html.Div(dcc.DatePickerRange(
            id='date-picker-range',
            start_date=covid_data["дата"].min(),
            end_date=covid_data["дата"].max(),
            display_format='YYYY-MM-DD',
        ), className="input-box-title"),
        html.Div(dcc.Dropdown(
            id='region-dropdown',
            options=city_options,
            value='Москва ',
            style={'height': '2em'}
        ), style={'width': '25%'})
    ], className="input-box"),

    html.Div([
        html.H2("Diseases Graph:")
    ], className="header-box"),
    dcc.Graph(id='diseases-graph'),

    html.Div([
        html.H2("Deaths Graph:")
    ], className="header-box"),
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

    start_date = np.datetime64(start_date)
    end_date = np.datetime64(end_date)

    filtered_data = covid_data[(covid_data["Регион "] == selected_region) & (covid_data["дата"] >= start_date) & (covid_data["дата"] <= end_date)]

    diseases_graph_figure = px.line(filtered_data, x='дата', y='случаи заболевания')
    deaths_graph_figure = px.line(filtered_data, x='дата', y='количество смертей')

    return diseases_graph_figure, deaths_graph_figure


if __name__ == '__main__':
    app.run_server(debug=True)
