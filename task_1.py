import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

airline_df = pd.read_csv('airline_data.csv')

external_stylesheets = ['/assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Lab 3, task 1'

app.layout = html.Div([
    html.Div([
        html.H1("Flight Delay Time Statistics", className="header"),
    ], className="header-box"),

    html.Div([
        html.Div(["Input Year:"], className="input-box-title"),
        dcc.Input(
            id='year-dropdown',
            placeholder='Enter a year...',
            type='number',
            value='2010',
            min='2010',
            max="2020"
        )], className="input-box"),

    html.Div([
        html.Div([
            dcc.Graph(id='carrier-delay-graph'),
            dcc.Graph(id='weather-delay-graph')
        ], style={'display': 'flex'}),

        html.Div([
            dcc.Graph(id='nas-delay-graph'),
            dcc.Graph(id='security-delay-graph')
        ], style={'display': 'flex'}),

        html.Div([
            dcc.Graph(id='late-aircraft-delay-graph')
        ])
    ])
])


def average_delay(df, delay_column):
    return df[['Month', 'Reporting_Airline', delay_column]].groupby(['Month', 'Reporting_Airline'])[
        delay_column].mean().reset_index()


@app.callback(
    [
        Output('carrier-delay-graph', 'figure'),
        Output('weather-delay-graph', 'figure'),
        Output('nas-delay-graph', 'figure'),
        Output('security-delay-graph', 'figure'),
        Output('late-aircraft-delay-graph', 'figure')
    ],
    [
        Input('year-dropdown', 'value')
    ]
)
def update_graphs(selected_year):
    year_data = airline_df[airline_df['Year'] == int(selected_year)]

    avg_carrier_delay = average_delay(year_data, 'CarrierDelay')
    avg_weather_delay = average_delay(year_data, 'WeatherDelay')
    avg_nas_delay = average_delay(year_data, 'NASDelay')
    avg_security_delay = average_delay(year_data, 'SecurityDelay')
    avg_late_aircraft_delay = average_delay(year_data, 'LateAircraftDelay')

    carrier_delay_figure = px.line(avg_carrier_delay, x='Month', y='CarrierDelay',
                                   color='Reporting_Airline',
                                   title='Average carrier delay time (minutes) by airline')

    weather_delay_figure = px.line(avg_weather_delay, x='Month', y='WeatherDelay',
                                   color='Reporting_Airline',
                                   title='Average weather delay time (minutes) by airline')

    nas_delay_figure = px.line(avg_nas_delay, x='Month', y='NASDelay',
                               color='Reporting_Airline',
                               title='Average NAS delay time (minutes) by airline')

    security_delay_figure = px.line(avg_security_delay, x='Month', y='SecurityDelay',
                                    color='Reporting_Airline',
                                    title='Average security delay time (minutes) by airline')

    late_aircraft_delay_figure = px.line(avg_late_aircraft_delay, x='Month', y='LateAircraftDelay',
                                         color='Reporting_Airline',
                                         title='Average late aircraft delay time (minutes) by airline')

    return carrier_delay_figure, weather_delay_figure, nas_delay_figure, security_delay_figure, late_aircraft_delay_figure


if __name__ == '__main__':
    app.run_server(debug=True)
