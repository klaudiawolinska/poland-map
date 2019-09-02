import pandas as pd
import chart_studio.tools
import chart_studio.plotly as py
import plotly.graph_objs as go


castles = pd.read_csv(r"clean_data/castles_clean.csv")
cities = pd.read_csv(r"clean_data/cities_clean.csv")
flixbus = pd.read_csv(r"clean_data/flixbus_clean.csv")
gardens = pd.read_csv(r"clean_data/gardens_clean.csv")
museums = pd.read_csv(r"clean_data/museums_clean.csv")
zoos = pd.read_csv(r"clean_data/zoos_clean.csv")

mapbox_access_token = ''  # fill in your access token from Mapbox

chart_studio.tools.set_credentials_file(username='', api_key='')  # fill in your Mapbox credentials

data = [
    go.Scattermapbox(
        lat=flixbus["latitude"],
        lon=flixbus["longitude"],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=10,
            color='rgb(4, 224, 88)',
            opacity=1
        ),
        text="►" + flixbus["city"],
        textposition='top center'
    ),
    go.Scattermapbox(
        lat=zoos["latitude"],
        lon=zoos["longitude"],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=9,
            color='rgb(89, 0, 255)',
            opacity=1
        ),
        text='ZOO: ' + zoos["name"],
        textposition='top center'
    ),
    go.Scattermapbox(
        lat=castles["lat"],
        lon=castles["long"],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=9,
            color='rgb(224, 173, 4)',
            opacity=1
        ),
        text="♜" + castles["castle"],
        textposition='top center'
    ),
    go.Scattermapbox(
        lat=gardens["latitude"],
        lon=gardens["longitude"],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=9,
            color='rgb(224, 4, 96)',
            opacity=1
        ),
        text="❀" + gardens["name"],
        textposition='top center'
    ),
    go.Scattermapbox(
        lat=museums["latitude"],
        lon=museums["longitude"],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=9,
            color='rgb(0, 0, 0)',
            opacity=1
        ),
        text="▣" + museums["museum"],
        textposition='top center'
    )
]

layout = go.Layout(
    title=' ',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=52.237049,
            lon=21.017532
        ),
        pitch=0,
        zoom=4.5,
        style='light'
    ),
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='poland-map')
