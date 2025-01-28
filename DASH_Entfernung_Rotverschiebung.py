import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

app = dash.Dash(__name__)

c = 299792.458  # km/s

beobachtete_z = [
    0.369, 0.000804, -0.000991, 0.158339, 0.055445, 0.019513, 0.001310, 0.002722, 0.1745, 0.34, 0.3751, 0.078720
]

beobachtete_entfernungen = [
    1380, 6.64, 0.682, 600, 235, 95, 8, 14.5, 720, 1020, 1464, 330
]

beobachtete_texte = [
    'Quasar 3C 48 (z=0.369, d=1380)', 'Galaxie MESSIER 101 (z=0.000804, d=6.64)', 'Andromeda M31 (z=-0.000991, d=0.682)',
    'Quasar 3C 273 (z=0.158339, d=600)', 'Galaxienhaufen Abell 85 (z=0.055445, d=235)', 'AGN Markarian 6 (z=0.019513, d=95)',
    'Galaxie MESSIER 51 (z=0.001310, d=8)', 'Galaxie NGC 7331 (z=0.002722, d=14.5)', 'Galaxienhaufen Abell 2218 (z=0.1745, d=720)',
    'GRB 130427A (z=0.34, d=1020)', 'Galaxienhaufen Abell 370 (z=0.375100, d=1464)', 'Abell 2029 (z=0.078720, d=330)'
]

# Layout der Dash-Anwendung
app.layout = html.Div([
    html.H1("Kosmologische Rotverschiebung in Abhängigkeit zur Entfernung", style={'font-family': 'Arial'}),
    
    # Wrapper für Slider und Eingabefeld nebeneinander
    html.Div([
        html.Div([
            html.Label("Hubble-Konstante (H0) in km/s/Mpc:", style={'font-size': 12, 'font-family': 'Arial'}),
            dcc.Slider(
                id='hubble-slider',
                min=50,
                max=625,
                step=1,
                value=70,
                marks={i: str(i) for i in range(50, 626, 50)},
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}),

        html.Div([
            html.Label("Eingabe:", style={'font-size': 12, 'font-family': 'Arial', 'margin': 'auto'}),
            dcc.Input(
                id='hubble-input',
                type='number',
                value=70,
                min=50,
                max=625,
                step=1,
                debounce=True,
                style={'width': '50px'}
            ),
        ], style={'width': '45%', 'display': 'inline-block'}),
    ], style={'text-align': 'center', 'margin-top': '50px', 'margin-bottom': '30px'}),
    
    # Der Graph für die Visualisierung
    dcc.Graph(id='z-graph'),
])

#Aktualisierung der Graphik 
@app.callback(
    Output('z-graph', 'figure'),
    [Input('hubble-slider', 'value'),
     Input('hubble-input', 'value')]
)
def update_graph(hubble_slider, hubble_input):
    # Vorrang des Eingabefelds
    hubble_constant = hubble_input if hubble_input is not None else hubble_slider

    # Entfernungen für die Berechnung der Rotverschiebung
    entfernungen = np.linspace(0, 1500, 100)
    
    # Berechnung der Rotverschiebung z
    z_values = (hubble_constant * entfernungen) / c
    
    # Erstellen des Graphen
    trace_z = go.Scatter(
        x=entfernungen,
        y=z_values,
        mode='lines',
        name=f'c * v = H0 * D' 
    )
    
    # Beobachtete Punkte für bekannte Objekte
    trace_observed = go.Scatter(
        x=beobachtete_entfernungen,
        y=beobachtete_z,
        mode='markers',
        name='Beobachtete Rotverschiebungen (Quelle: ned.ipac.caltech.edu)',
        marker=dict(color='red', size=8),
        text=beobachtete_texte,
        hoverinfo='text'
    )
    
    layout = go.Layout(
        title=f'Kosmologische Rotverschiebung (z) und Entfernung bei H0 = {hubble_constant} km/s/Mpc',
        xaxis={'title': 'Entfernung d (Mpc)'},
        yaxis={'title': 'Rotverschiebung z'},
        showlegend=True
    )
    
    return {'data': [trace_z, trace_observed], 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)