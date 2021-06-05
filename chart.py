import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
import plotly.graph_objs as go
import dash
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(f'history.csv')

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
    x=df.date,
    y=df.value,
    name="price",
), secondary_y=False)

fig.add_trace(go.Scatter(
    x=df.date,
    y=df.price,
    name="total value",
    yaxis="y2",
), secondary_y=True)

app.layout = html.Div(children=[

    dcc.Graph(
        id='price',
        figure=fig,
        style={'title': 'price vs supply', 'height': '1000px'}

    ),
],
)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True, dev_tools_hot_reload=True)
