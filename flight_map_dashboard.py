import random
from datetime import datetime, timedelta
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

df = pd.read_csv("flights_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

start_date = df['timestamp'].min().date()
end_date = df['timestamp'].max().date()

# Dash Application Setup
app = dash.Dash(__name__)
server = app.server

# Global variables for playback control
is_playing = False
current_time = df['timestamp'].min()
selected_flight = None

# Application Layout
app.layout = html.Div([
    # Main Header
    html.Div([
        html.H1("Flight Map", style={
            'textAlign': 'center', 
            'marginBottom': '20px',
            'marginTop': '0px',
            'color': 'green',
            'fontFamily': 'Courier, monospace',
            'position': 'absolute',
            'top': '10px',
            'left': '50%',
            'transform': 'translateX(-50%)',
            'zIndex': '1000'
        })
    ], style={'position': 'relative', 'zIndex': '1000'}),

    # Controls on the left side, positioned over the map
    html.Div([
        # Start date selection
        html.Label('Start:', style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.DatePickerSingle(
            id='start-date-picker',
            date=start_date,
            display_format='YYYY-MM-DD',
            style={
                'width': '100%',
                'marginBottom': '10px',
                'fontSize': '12px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),
        # Start time input field
        dcc.Input(
            id='start-time-input',
            type='text',
            value=df['timestamp'].min().strftime('%H:%M:%S'),
            placeholder='HH:MM:SS',
            style={
                'width': '100%',
                'height': '44px',  # Adjusted height to match DatePicker
                'marginBottom': '10px',
                'fontSize': '18px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),

        # End date selection
        html.Label('End:', style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.DatePickerSingle(
            id='end-date-picker',
            date=end_date,
            display_format='YYYY-MM-DD',
            style={
                'width': '100%',
                'marginBottom': '10px',
                'fontSize': '12px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),
        # End time input field
        dcc.Input(
            id='end-time-input',
            type='text',
            value=df['timestamp'].max().strftime('%H:%M:%S'),
            placeholder='HH:MM:SS',
            style={
                'width': '100%',
                'height': '40px',  # Adjusted height to match DatePicker
                'marginBottom': '10px',
                'fontSize': '18px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),

        # Playback speed control
        html.Label('Speed:  ', style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.Input(
            id='playback-speed-input',
            type='number',
            value=1,
            min=0.1,
            step=0.1,
            style={
                'width': '70%',
                'height': '40px',  # Adjusted height to match DatePicker
                'marginBottom': '10px',
                'fontSize': '16px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),

        # Map style selection
        html.Label('Map Style:', style={'fontSize': '16px', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='map-style-dropdown',
            options=[
                {'label': 'Open Street Map', 'value': 'open-street-map'},
                {'label': 'Carto Positron', 'value': 'carto-positron'},
                {'label': 'Carto Darkmatter', 'value': 'carto-darkmatter'},
            ],
            value='open-street-map',
            clearable=False,
            style={
                'width': '100%',
                'marginBottom': '10px',
                'fontSize': '16px',
                'backgroundColor': 'rgba(255, 255, 255, 0.5)',
                'border': 'none'
            }
        ),

        # Playback control buttons (Play, Pause, Restart)
        html.Div([
            html.Button('Play', id='play-button', n_clicks=0, style={
                'width': '30%', 'marginRight': '5%', 'fontSize': '16px',
                'backgroundColor': '#28a745', 'color': 'white',
                'border': 'none', 'borderRadius': '5px', 'padding': '10px',
                'cursor': 'pointer', 'transition': 'background-color 0.3s ease'
            }, 
            className="play-btn"),

            html.Button('Pause', id='pause-button', n_clicks=0, style={
                'width': '30%', 'marginRight': '5%', 'fontSize': '16px',
                'backgroundColor': '#ffc107', 'color': 'white',
                'border': 'none', 'borderRadius': '5px', 'padding': '10px',
                'cursor': 'pointer', 'transition': 'background-color 0.3s ease'
            }, 
            className="pause-btn"),

            html.Button('Restart', id='restart-button', n_clicks=0, style={
                'width': '30%', 'fontSize': '16px', 'textAlign': 'center',
                'backgroundColor': '#dc3545', 'color': 'white',
                'border': 'none', 'borderRadius': '5px', 'padding': '10px',
                'cursor': 'pointer', 'transition': 'background-color 0.3s ease'
            }, 
            className="restart-btn")
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}),
        
        # Flight info section (initially empty)
        html.Div(id='flight-info', style={
            'marginTop': '20px',
            'fontSize': '16px',
            'color': 'black',
            'backgroundColor': '#f9f9f9',
            'padding': '10px',
            'borderRadius': '5px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
    ], style={
        'position': 'absolute',
        'top': '150px',
        'left': '10px',
        'width': '220px',
        'backgroundColor': 'rgba(240, 240, 240, 0.9)',
        'padding': '10px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
        'zIndex': '1000'
    }),

    # Map and Visualization, set to full-screen size
    html.Div([
        dcc.Graph(id='live-map', config={
            'scrollZoom': True, 
            'displayModeBar': True, 
            'displaylogo': False, 
            'doubleClick': 'reset'  # Double click reset is enabled
        }, style={'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100vh'}),
        
        # Display the current date and time in digital clock style at the top left of the map
        html.Div(id='current-time-display', style={
            'position': 'absolute',
            'top': '10px',
            'left': '10px',
            'fontSize': '24px',
            'fontWeight': 'bold',
            'color': 'green',
            'fontFamily': 'Courier, monospace',
            'zIndex': '1000'
        })
    ], style={'position': 'relative'}),
    
    # Interval component for live updates
    dcc.Interval(
        id='interval-component',
        interval=2000,  # 2 seconds
        n_intervals=0
    ),
], style={'fontFamily': 'Arial, sans-serif', 'padding': '0', 'margin': '0', 'backgroundColor': '#ffffff', 'position': 'relative'})

# Callback to update the map, time display, and flight info
@app.callback(
    [Output('live-map', 'figure'),
     Output('current-time-display', 'children'),
     Output('flight-info', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('play-button', 'n_clicks'),
     Input('pause-button', 'n_clicks'),
     Input('restart-button', 'n_clicks'),
     Input('start-date-picker', 'date'),
     Input('start-time-input', 'value'),
     Input('end-date-picker', 'date'),
     Input('end-time-input', 'value'),
     Input('playback-speed-input', 'value'),
     Input('map-style-dropdown', 'value'),
     Input('live-map', 'clickData')],
    [State('live-map', 'figure')]
)
def update_map(n_intervals, play_clicks, pause_clicks, restart_clicks,
               start_date, start_time_input, end_date, end_time_input,
               playback_speed, map_style, clickData, existing_fig):
    global is_playing, current_time, selected_flight

    # Determine which button was clicked (Play, Pause, or Restart)
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'play-button':
        is_playing = True
    elif button_id == 'pause-button':
        is_playing = False
    elif button_id == 'restart-button':
        is_playing = True
        try:
            start_datetime = datetime.strptime(f"{start_date} {start_time_input}", '%Y-%m-%d %H:%M:%S')
            current_time = start_datetime
        except ValueError:
            current_time = df['timestamp'].min()
        selected_flight = None

    # Create a time range
    try:
        start_datetime = datetime.strptime(f"{start_date} {start_time_input}", '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(f"{end_date} {end_time_input}", '%Y-%m-%d %H:%M:%S')
    except ValueError:
        start_datetime = df['timestamp'].min()
        end_datetime = df['timestamp'].max()

    # Update current time according to playback speed
    if is_playing and button_id != 'restart-button':
        try:
            playback_speed = float(playback_speed)
        except (ValueError, TypeError):
            playback_speed = 1  # Default speed

        current_time += timedelta(seconds=playback_speed)
        if current_time > end_datetime:
            current_time = start_datetime
    else:
        pass  # Pause mode

    # Filter data up to the current time
    filtered_df = df[(df['timestamp'] <= current_time) &
                     (df['timestamp'] >= start_datetime) &
                     (df['timestamp'] <= end_datetime)]

    # Build the figure for the map
    fig = go.Figure()

    # Add flight points to the map
    for flight_id in filtered_df['callsign'].unique():
        flight_data = filtered_df[filtered_df['callsign'] == flight_id]
        latest_point = flight_data.iloc[-1]

        fig.add_trace(go.Scattermapbox(
            lat=[latest_point['latitude']],
            lon=[latest_point['longitude']],
            mode='markers',
            marker=go.scattermapbox.Marker(size=10),
            name=flight_id,
            customdata=[[latest_point['callsign'], latest_point['altitude'], latest_point['velocity']]],
            hovertemplate=
            "<b>%{customdata[0]}</b><extra></extra>",  # Only show flight ID
        ))

    # If a flight is selected and customdata exists, draw the route
    flight_info = "No flight selected"
    if clickData and 'points' in clickData and 'customdata' in clickData['points'][0]:
        selected_flight = clickData['points'][0]['customdata'][0]
        selected_flight_data = df[(df['callsign'] == selected_flight) & (df['timestamp'] <= current_time)]
        
        # Check if the selected_flight_data is empty
        if not selected_flight_data.empty:
            fig.add_trace(go.Scattermapbox(
                lat=selected_flight_data['latitude'],
                lon=selected_flight_data['longitude'],
                mode='lines',
                line=dict(width=2, color='red'),
                name=f"{selected_flight} Route",
                hoverinfo='none'
            ))

            # Show flight information in the control panel, rounded to 3 decimal places
            latest_point = selected_flight_data.iloc[-1]
            flight_info = html.Div([
                html.P([html.B("Callsign: "), f"{latest_point['callsign']}"]),
                html.P([html.B("Latitude: "), f"{round(latest_point['latitude'], 3)}"]),
                html.P([html.B("Longitude: "), f"{round(latest_point['longitude'], 3)}"]),
                html.P([html.B("Altitude: "), f"{round(latest_point['altitude'], 3)} m"]),
                html.P([html.B("Speed: "), f"{latest_point['velocity']} km/h"])
            ])
        else:
            flight_info = "No data available for this flight."

    # Maintain zoom and center settings, but allow map style changes
    zoom = 1
    center = dict(lat=0, lon=0)

    if existing_fig and 'mapbox' in existing_fig['layout']:
        zoom = existing_fig['layout']['mapbox'].get('zoom', 1)
        center = existing_fig['layout']['mapbox'].get('center', center)

    fig.update_layout(
        mapbox=dict(
            style=map_style,  # Update the map style dynamically
            zoom=zoom,
            center=center,
        ),
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=False,
        uirevision='mapstyle'  # Allow map style changes without reset
    )

    # Format the current time (including date and time)
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

    return fig, current_time_str, flight_info

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
