import plotly.graph_objects as go
import pandas as pd
import json

def load_atlas():
    with open("poets_atlas.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_poet_map(poet_name):
    data = load_atlas()
    stops = data.get(poet_name, [])
    if not stops:
        return None

    df = pd.DataFrame(stops)
    df['lat'] = df['coords'].apply(lambda x: x[0])
    df['lon'] = df['coords'].apply(lambda x: x[1])

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=df['lon'], lat=df['lat'],
        marker={'size': 12, 'color': '#8b7355'},
        line={'width': 2, 'color': '#8b7355'},
        text=df['year'] + " " + df['location'] + ": " + df['work'],
        hoverinfo='text'
    ))

    fig.update_layout(
        mapbox={
            'style': "stamen-terrain",
            'center': {'lon': 114, 'lat': 30},
            'zoom': 3
        },
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig