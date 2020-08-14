import os
import pathlib
import re
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from urllib.request import urlopen
import plotly.graph_objs as go
import cufflinks as cf

# Initialize app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

app = DjangoDash("dash_cb_4", external_stylesheets=external_stylesheets)

# app = dash.Dash(
#     __name__,
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
#     ],
# )
# server = app.server

# Load data
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

with open(os.path.join(APP_PATH, os.path.join('data/MB-reprojected.json'))) as response:
    MB_re = json.load(response)

with open(os.path.join(APP_PATH, os.path.join('data/AB-reprojected.json'))) as response:
    ab_re = json.load(response)

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_ca = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "ca.csv"))
)

df_lat_lon = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "lat_lon_counties.csv"))
)
df_lat_lon["FIPS "] = df_lat_lon["FIPS "].apply(lambda x: str(x).zfill(5))

df_full_data = pd.read_csv(
    os.path.join(
        APP_PATH, os.path.join("data", "age_adjusted_death_rate_no_quotes.csv")
    )
)
df_full_data["County Code"] = df_full_data["County Code"].apply(
    lambda x: str(x).zfill(5)
)
df_full_data["County"] = (
        df_full_data["Unnamed: 0"] + ", " + df_full_data.County.map(str)
)

#AB and MB
df_ab = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "AM", "ab", "ab_centroid.csv"))
)
dff_ab = pd.read_csv(
    os.path.join(
        APP_PATH, os.path.join("data", "AM", "ab", "yieldAB 2014-2018.csv")
    )
)

df_mb = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "AM", "mb", "mb_centroid.csv"))
)
dff_mb = pd.read_csv(
    os.path.join(
        APP_PATH, os.path.join("data", "AM", "mb", "yieldMB 2006-2018.csv")
    )
)





us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

YEARS = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
YEARS_1 = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

BINS = [
    "0-2",
    "2.1-4",
    "4.1-6",
    "6.1-8",
    "8.1-10",
    "10.1-12",
    "12.1-14",
    "14.1-16",
    "16.1-18",
    "18.1-20",
    "20.1-22",
    "22.1-24",
    "24.1-26",
    "26.1-28",
    "28.1-30",
    ">30",
]

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

my_tok = "pk.eyJ1IjoiYW9pZGgiLCJhIjoiY2p6d3ZlZnhuMHFtczNpcWlsM3pqbjZicCJ9.FOWwd5ipYbL_9Kf670Loug"
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout

app.layout = html.Div(
    id="root",
    children=[
# Below here it is a sample body
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                html.H4(children="Rate of US Poison-Induced Deaths"),
                html.P(
                    id="description",
                    children="† Deaths are classified using the International Classification of Diseases, \
                    Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying \
                    cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 \
                    (undetermined intent).",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        } for year in YEARS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap of age adjusted mortality rates \
                            from poisonings in year {0}".format(
                                        min(YEARS)
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=dict(
                                        data=[
                                            dict(
                                                lat=df_lat_lon["Latitude "],
                                                lon=df_lat_lon["Longitude"],
                                                text=df_lat_lon["Hover"],
                                                type="scattermapbox",
                                            )
                                        ],
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=38.72490, lon=-95.61446
                                                ),
                                                pitch=0,
                                                zoom=3.5,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Histogram of total number of deaths (single year)",
                                    "value": "show_absolute_deaths_single_year",
                                },
                                {
                                    "label": "Histogram of total number of deaths (1999-2016)",
                                    "value": "absolute_deaths_all_time",
                                },
                                {
                                    "label": "Age-adjusted death rate (single year)",
                                    "value": "show_death_rate_single_year",
                                },
                                {
                                    "label": "Trends in age-adjusted death rate (1999-2016)",
                                    "value": "death_rate_all_time",
                                },
                            ],
                            value="show_death_rate_single_year",
                            id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            dcc.Graph(
                id="dcc_t_2",
                figure=dict(
                    data=[
                        dict(
                            lat=df_ca["lat"],
                            lon=df_ca["lng"],
                            type="scattermapbox",
                        )
                    ],
                    layout=dict(
                        mapbox=dict(
                            layers=[
                                {
                                    "below": 'traces',
                                    "sourcetype": "raster",
                                    "source": [
                                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                                    ]
                                },
                            ],
                            # style="dark",
                            # style="white-bg",
                            accesstoken=mapbox_access_token,
                            # style="dark",
                            center=dict(
                                lat=49.883333, lon=-97.166667
                            ),
                            pitch=0,
                            zoom=3,
                        ),
                        autosize=True,
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    ),
                ),

            ),
        ),
        html.Div(
            dcc.Slider(
                id="y-slider",
                min=min(YEARS_1),
                max=max(YEARS_1),
                value=min(YEARS_1),
                marks={
                    str(year): {
                        "label": str(year),
                        "style": {"color": "#7fafdf"},
                    } for year in YEARS_1
                },
            ),
            style={'padding': 50}
        ),
        html.Div(
            id="gra-container",
            children=[
                html.H4(children="Alberta"),
                dcc.Dropdown(
                    options=[
                        {
                            "label": "AB_Canola Dryland TOTAL ACREAGE(Single year)",
                            "value": "dryland_total_single",
                        },
                        {
                            "label": "AB_Canola Dryland WEIGHTED AVERAGE YIELD(single year)",
                            "value": "dryland_weight_single",
                        },
                        {
                            "label": "AB_Canola Dryland TOTAL ACREAGE(all year)",
                            "value": "dryland_total_all",
                        },
                    ],
                    value="dryland_total_single",
                    id="c-dropdown",
                ),
                html.H4(children="Manitoba"),
                dcc.Dropdown(
                    options=[
                        {
                            "label": "MB_Canola Dryland TOTAL ACREAGE(Single year)",
                            "value": "canola_total_single",
                        },
                        {
                            "label": "MB_Canola Dryland WEIGHTED AVERAGE YIELD(single year)",
                            "value": "canola_weight_single",
                        },
                        {
                            "label": "MB_Canola Dryland TOTAL ACREAGE(all year)",
                            "value": "canola_total_all",
                        },
                    ],
                    value="canola_total_single",
                    id="mb-dropdown",
                ),
                html.H1(children="AB 2014-2018 & MB 2006-2018"),
                dcc.Graph(
                    id="s-data",
                    figure=dict(
                        data=[dict(x=0, y=0)],
                        layout=dict(
                            paper_bgcolor="#F4F4F8",
                            plot_bgcolor="#F4F4F8",
                            autofill=True,
                            margin=dict(t=75, r=50, b=100, l=50),
                        ),
                    ),
                ),
            ]
        ),

        html.Div(
            dcc.Graph(
                id="dcc_t_1",
                figure=dict(
                    data=[
                        dict(
                            lat=us_cities["lat"],
                            lon=us_cities["lon"],
                            # lat=df_lat_lon["Latitude "],
                            # lon=df_lat_lon["Longitude"],
                            # text=df_lat_lon["Hover"],
                            type="scattermapbox",
                        )
                    ],
                    layout=dict(
                        mapbox=dict(
                            layers=[],
                            style="dark",
                            accesstoken=mapbox_access_token,
                            # style="dark",
                            center=dict(
                                lat=38.72490, lon=-95.61446
                            ),
                            pitch=0,
                            zoom=3,
                        ),
                        autosize=True,
                        # margin={"r":0,"t":0,"l":0,"b":0},
                    ),
                ),

            ),
        ),
    ],
)


@app.callback(
    Output("dcc_t_2", "figure"),
    [Input("years-slider", "value")]
)
def show_grid(year):
    data = [
        dict(
            lon=df_ab["xcoord"],
            lat=df_ab["ycoord"],
            text=df_ab["layer"],
            type="scattermapbox",
        ),
        dict(
            lon=df_mb["xcoord"],
            lat=df_mb["ycoord"],
            text=df_mb["ADMIN_BOUN"],
            type="scattermapbox",
        )
    ]

    base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
    layout = dict(
        mapbox=dict(
            layers=[
                dict(
                    # below="traces",
                    sourcetype="geojson",
                    source=ab_re,
                    type="fill",
                    color="#f2fffb",
                    opacity=DEFAULT_OPACITY,
                    # CHANGE THIS
                    fill=dict(outlinecolor="#afafaf"),
                ),
            ],
            style="dark",
            # accesstoken=mapbox_access_token,
            accesstoken=my_tok,
            # style="dark",

            center=dict(
                lat=55.883333, lon=-97.166667
            ),

            pitch=0,
            zoom=3,
        ),
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    mb_layer = dict(
        sourcetype="geojson",
        source=MB_re,
        type="fill",
        color="#f2fffb",
        opacity=DEFAULT_OPACITY,
        # CHANGE THIS
        fill=dict(outlinecolor="#afafaf"),
    )
    layout["mapbox"]["layers"].append(mb_layer)

    geo_layer = dict(
        below="traces",
        sourcetype="raster",
        source=["https://geo.weather.gc.ca/geomet/?"
                   "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                   "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
        type="fill",
        color="#f2fffb",
        opacity=DEFAULT_OPACITY,
        # CHANGE THIS
        fill=dict(outlinecolor="#afafaf"),
    )
    layout["mapbox"]["layers"].append(geo_layer)

    fig = dict(data=data, layout=layout)
    return fig


@app.callback(
    Output("s-data", "figure"),
    [
        Input("dcc_t_2", "selectedData"),
        Input("c-dropdown", "value"),
        Input("mb-dropdown", "value"),
        Input("y-slider", "value")
    ],
)
def update_AB_MB(selectedData, chart_dropdown, mb_dropdown, year):
    if selectedData is None:
        return dict(
            data=[dict(x=0, y=0)],
            layout=dict(
                title="Click-drag on the map to select counties",
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                margin=dict(t=75, r=50, b=100, l=75),
            ),
        )
    # get the riskzone from selected data
    pts = selectedData["points"]
    rzs = [str(pt["text"]) for pt in pts]

    #AB
    # filter with rzs
    dff = dff_ab[dff_ab["riskzone"].isin(rzs)]
    dff = dff.sort_values("year")

    # replace the empty column
    regex_pat = re.compile(r"Unreliable", flags=re.IGNORECASE)
    dff["Canola Dryland TOTAL ACREAGE "] = dff["Canola Dryland TOTAL ACREAGE "].replace(regex_pat, 0)
    dff["Canola Dryland WEIGHTED AVERAGE YIELD "] = dff["Canola Dryland WEIGHTED AVERAGE YIELD "].replace(regex_pat, 0)

    if chart_dropdown == "dryland_weight_single":
        dff = dff[dff.year == year]
        title = "Canola Dryland WEIGHTED AVERAGE YIELD {}".format(year)
        AGGREGATE_BY = "Canola Dryland WEIGHTED AVERAGE YIELD "

    if chart_dropdown == "dryland_total_single":
        dff = dff[dff.year == year]
        title = "Canola Dryland TOTAL AVERAGE in a single year {}".format(year)
        AGGREGATE_BY = "Canola Dryland TOTAL ACREAGE "

    if chart_dropdown == "dryland_total_all":
        dff["riskzone"] = pd.to_numeric(dff["riskzone"], errors="coerce")
        list_dff = []
        for i in range(1, 23):
            list_dff.append(dff[dff.riskzone == i])
        data = []
        for i in range(22):
            dict_add = dict(
                type="area",
                x=list_dff[i]["year"],
                y=list_dff[i]["Canola Dryland TOTAL ACREAGE "],
                colors="#1b9e77",
            )
            data.append(dict_add)

        layout = dict()
        fig = dict(data=data, layout=layout)

        fig["layout"]["legend"] = dict(orientation="v")
        fig["layout"]["autosize"] = True
        fig["layout"]["paper_bgcolor"] = "#1f2630"
        fig["layout"]["plot_bgcolor"] = "#1f2630"
        return fig

    # and combine with riskzone
    dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
    dff = dff.groupby("riskzone")[AGGREGATE_BY].sum()

    # MB
    # if AB poins selected, MB will cover
    if dff.empty:
        dff = dff_mb[dff_mb["ADMIN_BOUN"].isin(rzs)]
        dff = dff.sort_values("year")

        # replace the empty column
        regex_pat = re.compile(r"Unreliable", flags=re.IGNORECASE)
        dff["Canola TOTAL ACREAGE "] = dff["Canola TOTAL ACREAGE "].replace(regex_pat, 0)
        dff["Canola WEIGHTED AVERAGE YIELD "] = dff["Canola WEIGHTED AVERAGE YIELD "].replace(regex_pat, 0)

        if mb_dropdown == "canola_weight_single":
            dff = dff[dff.year == year]
            title = "Canola WEIGHTED AVERAGE YIELD {}".format(year)
            AGGREGATE_BY = "Canola WEIGHTED AVERAGE YIELD "

        if mb_dropdown == "canola_total_single":
            dff = dff[dff.year == year]
            title = "Canola TOTAL AVERAGE in a single year {}".format(year)
            AGGREGATE_BY = "Canola TOTAL ACREAGE "

        if mb_dropdown == "canola_total_all":
            # dff["ADMIN_BOUN"] = pd.to_numeric(dff["ADMIN_BOUN"], errors="coerce")
            list_dff_2 = []
            for i in range(1, 17):
                list_dff_2.append(dff[dff.ADMIN_BOUN == f"RSA{i:02d}"])

            data = []
            for i in range(16):
                dict_add = dict(
                    type="area",
                    x=list_dff_2[i]["year"],
                    y=list_dff_2[i]["Canola TOTAL ACREAGE "],
                    colors="#1b9e77",
                )
                data.append(dict_add)
            layout = dict()
            fig = dict(data=data, layout=layout)
            return fig


        dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
        # it will convert to pandas.Series, not dataframe
        dff = dff.groupby("ADMIN_BOUN")[AGGREGATE_BY].sum()

    dff = dff.sort_values()
    # Only look at non-zero rows:
    dff = dff[dff > 0]

    # fig = dff.iplot(
    #     kind="bar", y=AGGREGATE_BY, title=title, asFigure=True
    # )

    data = [
        dict(
            x=dff.index,
            y=dff,
            type="bar",
            marker=dict(
                color="#2cfec1",
                opacity=1,
                textposition="outside",
            )
        )
    ]
    layout = dict(
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font_color="#2cfec1",
    )
    fig=dict(data=data, layout=layout)


    # fig_layout = fig["layout"]
    # fig_data = fig["data"]
    #
    # fig_data[0]["text"] = dff.values.tolist()
    # fig_data[0]["marker"]["color"] = "#2cfec1"
    # fig_data[0]["marker"]["opacity"] = 1
    # fig_data[0]["marker"]["line"]["width"] = 0
    # fig_data[0]["textposition"] = "outside"
    # fig_layout["paper_bgcolor"] = "#1f2630"
    # fig_layout["plot_bgcolor"] = "#1f2630"
    # fig_layout["font"]["color"] = "#2cfec1"
    # fig_layout["title"]["font"]["color"] = "#2cfec1"
    # fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    # fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    # fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    # fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    # fig_layout["margin"]["t"] = 75
    # fig_layout["margin"]["r"] = 50
    # fig_layout["margin"]["b"] = 100
    # fig_layout["margin"]["l"] = 50

    return fig

@app.callback(
    Output("dcc_t_1", "figure"),
    [Input("years-slider", "value")]
)
def show_grid(year):
    data = [
        dict(
            # lat=df_ca["lat"],
            # lon=df_ca["lng"],
            # lat=us_cities["lat"],
            # lon=us_cities["lon"],

            lat=df_lat_lon["Latitude "],
            lon=df_lat_lon["Longitude"],
            text=df_lat_lon["Hover"],
            type="scattermapbox",
        )
    ]
    # fig = px.scatter_mapbox(
    #     df_lat_lon,
    #     lat="Latitude ",
    #     lon="Longitude",
    #     text="Hover"
    # )

    cm = dict(zip(BINS, DEFAULT_COLORSCALE))
    base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
    layout = dict(
        mapbox=dict(
            layers=[
                dict(
                    sourcetype="geojson",
                    source="https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/2010/0-2.geojson",
                    type="fill",
                    color="#630964",
                    opacity=DEFAULT_OPACITY,
                    # CHANGE THIS
                    fill=dict(outlinecolor="#afafaf"),
                ),
                {
                    "sourcetype": "raster",
                    "source": ["https://geo.weather.gc.ca/geomet/?"
                               "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                               "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
                },
            ],
            # style="dark",
            # style="basic",
            style="satellite",

            # style="white-bg",
            # style="stamen-terrain",
            # style="white-bg",
            accesstoken=mapbox_access_token,
            # style="dark",
            center=dict(
                lat=38.72490, lon=-95.61446
            ),
            pitch=0,
            zoom=3,
        ),
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    fig = dict(data=data, layout=layout)
    return fig

# Below it is the sample callback function from dash gallery
@app.callback(
    Output("county-choropleth", "figure"),
    [Input("years-slider", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(year, figure):
    cm = dict(zip(BINS, DEFAULT_COLORSCALE))

    data = [
        dict(
            lat=df_lat_lon["Latitude "],
            lon=df_lat_lon["Longitude"],
            text=df_lat_lon["Hover"],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=5, color="white", opacity=0),
        )
    ]

    annotations = [
        dict(
            showarrow=False,
            align="right",
            text="<b>Age-adjusted death rate<br>per county per year</b>",
            font=dict(color="#2cfec1"),
            bgcolor="#1f2630",
            x=0.95,
            y=0.95,
        )
    ]

    for i, bin in enumerate(reversed(BINS)):
        color = cm[bin]
        annotations.append(
            dict(
                arrowcolor=color,
                text=bin,
                x=0.95,
                y=0.85 - (i / 20),
                ax=-60,
                ay=0,
                arrowwidth=5,
                arrowhead=0,
                bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
            )
        )

    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = (38.72490,)
        lon = (-95.61446,)
        zoom = 3.5

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            # style="dark",
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=annotations,
        dragmode="lasso",
    )

    base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
    for bin in BINS:
        geo_layer = dict(
            sourcetype="geojson",
            source=base_url + str(year) + "/" + bin + ".geojson",
            type="fill",
            color=cm[bin],
            opacity=DEFAULT_OPACITY,
            # CHANGE THIS
            fill=dict(outlinecolor="#afafaf"),
        )
        layout["mapbox"]["layers"].append(geo_layer)

    fig = dict(data=data, layout=layout)
    return fig


@app.callback(Output("heatmap-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Heatmap of age adjusted mortality rates \
				from poisonings in year {0}".format(year)


@app.callback(
    Output("selected-data", "figure"),
    [
        Input("county-choropleth", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_dat(selectedData, chart_dropdown, year):
    if selectedData is None:
        return dict(
            data=[dict(x=0, y=0)],
            layout=dict(
                title="Click-drag on the map to select counties",
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                margin=dict(t=75, r=50, b=100, l=75),
            ),
        )
    # get the fips from selected data, to get the FIPS
    pts = selectedData["points"]
    fips = [str(pt["text"].split("<br>")[-1]) for pt in pts]
    for i in range(len(fips)):
        if len(fips[i]) == 4:
            fips[i] = "0" + fips[i]

    # filter with FIPS
    dfff = df_full_data[df_full_data["County Code"].isin(fips)]
    dff = dfff.sort_values("Year")

    # replace the empty column
    regex_pat = re.compile(r"Unreliable", flags=re.IGNORECASE)
    dff["Age Adjusted Rate"] = dff["Age Adjusted Rate"].replace(regex_pat, 0)

    if chart_dropdown != "death_rate_all_time":
        title = "Absolute deaths per county, <b>1999-2016</b>"
        AGGREGATE_BY = "Deaths"
        if "show_absolute_deaths_single_year" == chart_dropdown:
            dff = dff[dff.Year == year]
            title = "Absolute deaths per county, <b>{0}</b>".format(year)
        elif "show_death_rate_single_year" == chart_dropdown:
            dff = dff[dff.Year == year]
            title = "Age-adjusted death rate per county, <b>{0}</b>".format(year)
            AGGREGATE_BY = "Age Adjusted Rate"

        dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
        deaths_or_rate_by_fips = dff.groupby("County")[AGGREGATE_BY].sum()
        deaths_or_rate_by_fips = deaths_or_rate_by_fips.sort_values()
        # Only look at non-zero rows:
        deaths_or_rate_by_fips = deaths_or_rate_by_fips[deaths_or_rate_by_fips > 0]
        data = [
            dict(
                x=deaths_or_rate_by_fips.index,
                y=deaths_or_rate_by_fips,
                # x=dff["year"],
                # y=dff[AGGREGATE_BY],
                type="bar",
                text=deaths_or_rate_by_fips.values.tolist(),
                marker=dict(
                    color="#2cfec1",
                    opacity=1,
                    textposition="outside",
                    line=dict(
                        width=0,
                    )
                )
            )
        ]
        layout = dict(
            title=title,
            paper_bgcolor="#1f2630",
            plot_bgcolor="#1f2630",
            font=dict(color="#2cfec1"),
            title_font=dict(color="#2cfec1"),
            xaxis=dict(
                tickfont=dict(color="#2cfec1"),
                gridcolor="#5b5b5b",
            ),
            yaxis=dict(
                tickfont=dict(color="#2cfec1"),
                gridcolor="#5b5b5b",
            ),
            margin=dict(
                t=75,
                r=50,
                b=100,
                l=50,
            )

        )
        fig = dict(data=data, layout=layout)
        # ************************************plotly 3.10.0, cufflinks************************
        # fig = deaths_or_rate_by_fips.iplot(
        #     kind="bar", y=AGGREGATE_BY, title=title, asFigure=True
        # )
        #
        # fig_layout = fig["layout"]
        # fig_data = fig["data"]
        #
        # fig_data[0]["text"] = deaths_or_rate_by_fips.values.tolist()
        # fig_data[0]["marker"]["color"] = "#2cfec1"
        # fig_data[0]["marker"]["opacity"] = 1
        # fig_data[0]["marker"]["line"]["width"] = 0
        # fig_data[0]["textposition"] = "outside"
        # fig_layout["paper_bgcolor"] = "#1f2630"
        # fig_layout["plot_bgcolor"] = "#1f2630"
        # fig_layout["font"]["color"] = "#2cfec1"

        # fig_layout["title"]["font"]["color"] = "#2cfec1"
        # fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
        # fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
        # fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
        # fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
        # fig_layout["margin"]["t"] = 75
        # fig_layout["margin"]["r"] = 50
        # fig_layout["margin"]["b"] = 100
        # fig_layout["margin"]["l"] = 50
        # ************************************************************************
        return fig
    # ************************************plotly 4.10.1************************
    length = int(dfff.shape[0])
    end = int(dfff.shape[0]/18)
    list_dff = []
    i = 0
    while i < length:
        list_dff.append(dfff.iloc[i:i+17, :])
        i = i + 18
    data = []
    for i in range(end):
        dict_add = dict(
            type="area",
            x=list_dff[i]["Year Code"],
            y=list_dff[i]["Age Adjusted Rate"],
            colors="#1b9e77",
            name=list_dff[i].iloc[0, 0],
            marker=dict(
                opacity=0.5,
                textposition="outside",
            )
        )
        data.append(dict_add)
    layout = dict(
        title = "<b>{0}</b> counties selected".format(int(end)),
        legend=dict(orientation="v"),
        autosize=True,
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        title_font=dict(color="#2cfec1"),
        xaxis=dict(
            tickfont=dict(color="#2cfec1"),
            gridcolor="#5b5b5b",
        ),
        yaxis=dict(
            tickfont=dict(color="#2cfec1"),
            gridcolor="#5b5b5b",
        ),
        margin=dict(
            t=75,
            r=50,
            b=100,
            l=50,
        )

    )
    fig=dict(data=data, layout=layout)
    fig["data"] = fig["data"][0:500]
    # ************************************plotly 3.10.0, cufflinks************************
    # fig = dff.iplot(
    #     kind="area",
    #     x="Year",
    #     y="Age Adjusted Rate",
    #     text="County",
    #     categories="County",
    #     colors=[
    #         "#1b9e77",
    #         "#d95f02",
    #         "#7570b3",
    #         "#e7298a",
    #         "#66a61e",
    #         "#e6ab02",
    #         "#a6761d",
    #         "#666666",
    #         "#1b9e77",
    #     ],
    #     vline=[year],
    #     asFigure=True,
    # )
    #
    # for i, trace in enumerate(fig["data"]):
    #     trace["mode"] = "lines+markers"
    #     trace["marker"]["size"] = 4
    #     trace["marker"]["line"]["width"] = 1
    #     trace["type"] = "scatter"
    #     for prop in trace:
    #         fig["data"][i][prop] = trace[prop]
    #
    # # Only show first 500 lines
    # fig["data"] = fig["data"][0:500]
    #
    # fig_layout = fig["layout"]
    #
    # # See plot.ly/python/reference
    # fig_layout["yaxis"]["title"] = "Age-adjusted death rate per county per year"
    # fig_layout["xaxis"]["title"] = ""
    # fig_layout["yaxis"]["fixedrange"] = True
    # fig_layout["xaxis"]["fixedrange"] = False
    # fig_layout["hovermode"] = "closest"
    # fig_layout["title"] = "<b>{0}</b> counties selected".format(len(fips))
    # fig_layout["legend"] = dict(orientation="v")
    # fig_layout["autosize"] = True
    # fig_layout["paper_bgcolor"] = "#1f2630"
    # fig_layout["plot_bgcolor"] = "#1f2630"
    # fig_layout["font"]["color"] = "#2cfec1"
    # fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    # fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    # fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    # fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    # ************************************************************************

    if len(fips) > 500:
        fig["layout"][
            "title"
        ] = "Age-adjusted death rate per county per year <br>(only 1st 500 shown)"

    return fig

#
# if __name__ == "__main__":
#     app.run_server(debug=True)
