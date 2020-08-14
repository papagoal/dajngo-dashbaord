import dash
import dash_core_components as dcc
import dash_html_components as html
import  pandas as pd
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pathlib
import os
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = DjangoDash("SimpleExample5", external_stylesheets=external_stylesheets)

# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/' +
#     '5d1ea79569ed194d432e56108a04d188/raw/' +
#     'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#     'gdp-life-exp-2007.csv')

# df = pd.read_csv("/Users/danliu/Desktop/AIRM/0812/website_2/a_thing/dash_collection/files/2007.csv")
df = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("files", "2007.csv"))
)
# print(df)
markdown_text= '''
# Dash and Markdown

I can write whatever I want
Thank you
'''
app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data':[
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capital'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    dcc.Markdown(children=markdown_text)
])
