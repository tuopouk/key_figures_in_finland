# -*- coding: utf-8 -*-
import pandas as pd
from dash_extensions.enrich import (
    dcc,
    html,
    Input,
    Output,
    State,
    Serverside,
    register_page,
    callback,
    clientside_callback,
)
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO
import plotly.express as px
import orjson
import requests
from dash.exceptions import PreventUpdate
import re

register_page(
    __name__,
    path="/",
    title="Key Figures Finland",
    name="Key Figures Finland",
    description="Visualizing Finland's Key Figures",
    image="en.png",
    redirect_from=["/assets", "/assets/"],
)

config = {"locale": "en"}

fig_df = pd.DataFrame([{"x": 0, "y": 0, "text": "Loading timeseries..."}])
default_fig = px.scatter(fig_df, x="x", y="y", text="text")
default_fig.update_traces(mode="text", textfont_size=25)
default_fig.update_xaxes(showgrid=False, visible=False)
default_fig.update_yaxes(showgrid=False, visible=False)

token = open(".mapbox_token").read()
default_map = px.choropleth_mapbox(
    center={"lat": 64.961093, "lon": 25.795386},
    zoom=3.8,
    height=600,
    mapbox_style="open-street-map"
)
default_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

definitions = pd.read_csv("./assets/definitions_en.csv").set_index("key_figure")


def get_data(region_level):

    name = "name"

    # Query url
    url = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/Kuntien_avainluvut/uusin/kuntien_avainluvut_viimeisin.px"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "application/json",
    }

    with open(f"./assets/{region_level}_payload.json") as f:
        payload = orjson.loads(f.read())

    json = requests.post(url, json=payload, headers=headers).json()

    cities = list(json["dimension"]["Alue"]["category"]["label"].values())
    if region_level != 'Municipality':
        cities = [cities[0]]+[' '.join(c.split()[1:]).strip() for c in cities[1:]]
   

    dimensions = list(json["dimension"]["Tiedot"]["category"]["label"].values())

    values = json["value"]

    cities_df = pd.DataFrame(cities, columns=[name])
    cities_df["index"] = 0
    dimensions_df = pd.DataFrame(dimensions, columns=["dimensions"])
    dimensions_df["index"] = 0

    data = pd.merge(left=cities_df, right=dimensions_df, on="index", how="outer").drop(
        "index", axis=1
    )
    data["value"] = values
    data = pd.pivot_table(data, values="value", index=[name], columns="dimensions")
    data = data.reset_index()
    data["region_level"] = region_level
    data = data.set_index("region_level")
    data.index = data.index.astype("category")
    
    data[name] = data[name].astype("category")
    
    return data


data_df = pd.concat(
    [get_data("Region"), 
     get_data("Sub-region").query("name!='WHOLE COUNTRY'"), 
     get_data("Municipality").query("name!='WHOLE COUNTRY'")]
)


whole_country_df = pd.DataFrame(
    data_df.set_index("name").loc["WHOLE COUNTRY"].sort_index()
)

whole_country_df["year"] = [stat.split(", ")[-1] for stat in whole_country_df.index]
whole_country_df["unit"] = [
    stat.split(", ")[-2] if len(stat.split(", ")) > 2 else ""
    for stat in whole_country_df.index
]
whole_country_df["stat_name"] = [
    stat.split(", ")[0]
    if len(stat.split(", ")) < 4
    else ", ".join(stat.split(", ")[:2])
    for stat in whole_country_df.index
]
data_df = data_df[data_df.name != "WHOLE COUNTRY"]


layout = dbc.Container(
    [
        html.H1("Finland's Key Figures", className="fw-bold display-1 text-center"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H2("Key figure"),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-key-figure-selection-en",
                                                            options=whole_country_df.index,
                                                            value=whole_country_df.index[
                                                                0
                                                            ],
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H2("Regional level"),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-region-selection-en",
                                                            options=[
                                                                "Region",
                                                                "Sub-region",
                                                                "Municipality",
                                                            ],
                                                            value="Region",
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        html.Div(
                                            id="key-figures-finland-whole-country-header-en",
                                            className="text-center card-title mt-5 mb-3",
                                        ),
                                        dcc.Graph(
                                            id="key-figures-finland-timeseries-en",
                                            className="border",
                                            figure=default_fig,
                                            config=config,
                                        ),
                                        dcc.Loading(
                                            [
                                                dcc.Store(
                                                    id="key-figures-finland-series-data-region-en"
                                                ),
                                                dcc.Store(
                                                    id="key-figures-finland-series-data-subregion-en"
                                                ),
                                                dcc.Store(
                                                    id="key-figures-finland-series-data-municipality-en"
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            "Change chart type",
                                                            className="mt-2",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-chart-selection-en",
                                                            options=["area", "line"],
                                                            value="line",
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            "Change chart template",
                                                            className="mt-2",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-chart-template-en",
                                                            options=sorted(
                                                                [
                                                                    "bootstrap_theme",
                                                                    "plotly",
                                                                    "ggplot2",
                                                                    "seaborn",
                                                                    "simple_white",
                                                                    "plotly_white",
                                                                    "plotly_dark",
                                                                    "presentation",
                                                                    "xgridoff",
                                                                    "ygridoff",
                                                                    "gridon",
                                                                    "none",
                                                                ]
                                                            ),
                                                            value="bootstrap_theme",
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.CardFooter(
                                    [
                                        "Data by ",
                                        html.A(
                                            "Statistics Finland",
                                            href="https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/",
                                            target="_blank",
                                        ),
                                    ],
                                    className="text-center align-middle card-text fs-3 text mt-3",
                                ),
                            ],
                            style={"height": "100%"},
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=6,
                    lg=6,
                    xl=6,
                    xxl=6,
                    align="start",
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H1(
                                            id="key-figures-finland-header-en",
                                            className="mb-3 mt-3 display-3 card-title text-center",
                                        ),
                                        dcc.Loading(
                                        dcc.Graph(
                                            id="key-figures-finland-region-map-en",
                                            figure=default_map,
                                            clear_on_unhover=True,
                                            config={
                                                "mapboxAccessToken": token,
                                                "locale": "en",
                                            },
                                            className="border",
                                        )),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            "Change map type",
                                                            className="mt-2",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-map-type-en",
                                                            options=sorted(
                                                                [
                                                                 "open-street-map",
                                                                    "carto-positron",
                                                                    "carto-darkmatter",
                                                                    "basic",
                                                                    "streets",
                                                                    "outdoors",
                                                                    "light",
                                                                    "dark",
                                                                    "satellite",
                                                                    "satellite-streets",
                                                                    "white-bg"
                                                                ]
                                                            ),
                                                            value="open-street-map",
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            "Change colorscale",
                                                            className="mt-2",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="key-figures-finland-map-colorscale-en",
                                                            options=sorted(
                                                                [
                                                                    "Blackbody",
                                                                    "Bluered",
                                                                    "Blues",
                                                                    "Cividis",
                                                                    "Earth",
                                                                    "Electric",
                                                                    "Greens",
                                                                    "Greys",
                                                                    "Hot",
                                                                    "Jet",
                                                                    "Picnic",
                                                                    "Portland",
                                                                    "Rainbow",
                                                                    "RdBu",
                                                                    "Reds",
                                                                    "Viridis",
                                                                    "YlGnBu",
                                                                    "YlOrRd"
                                                                    
                                                                ]
                                                            ),
                                                            value="RdBu",
                                                            className="text-nowrap",
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                html.P(
                                                    id="key-figures-finland-definition-en",
                                                    children=definitions.loc[
                                                        whole_country_df.index[0].split(
                                                            ","
                                                        )[0]
                                                    ].definition,
                                                    className="card-text mt-3 mb-2",
                                                ),
                                                html.Div(
                                                    id="key-figures-finland-audio-en"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            style={"height": "100%"},
                        )
                    ],
                    xs=12,
                    sm=12,
                    md=6,
                    lg=6,
                    xl=6,
                    xxl=6,
                ),
            ],
            justify="center",
            className="mt-3 d-flex justify-content-center",
        ),
        dcc.Store(id="key-figures-finland-geojson-data-en"),
        dcc.Store(id="key-figures-finland-locations-en"),
        dcc.Store(id="key-figures-finland-zs-en"),
    ],
    fluid=True,
)


@callback(
    Output("key-figures-finland-audio-en", "children"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
)
def update_playback(key_word):
    kw = re.sub(r"\W+", "", key_word.split(",")[0])
    return html.Audio(
        src=f"./assets/recordings/en/{kw}.mp3",
        controls=True,
        autoPlay=False,
        title="Read outloud",
    )


@callback(
    Output("key-figures-finland-definition-en", "children"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
)
def update_definition(key_figure):
    try:
        return definitions.loc[key_figure.split(",")[0]].definition
    except:
        return ""


@callback(
    Output("key-figures-finland-series-data-region-en", "data"),
    Input("key-figures-finland-series-data-region-x", "data"),
    State("key-figures-finland-region-names-x", "data"),
    State("key-figures-finland-series-indicator-names-x", "data"),
)
def create_reg_timeseries_data(region_df, reg_names, series_indicator_names):
    def apply_index_name(index):
        return reg_names.loc[index]["name"]

    def apply_indicator_name(index):
        return series_indicator_names.loc[index]["name"]
    
    region_df.index = region_df.index.map(apply_index_name)
    region_df.dimensions = region_df.dimensions.map(apply_indicator_name)
    
    return Serverside(region_df)


@callback(
    Output("key-figures-finland-series-data-subregion-en", "data"),
    Input("key-figures-finland-series-data-subregion-x", "data"),
    State("key-figures-finland-region-names-x", "data"),
    State("key-figures-finland-series-indicator-names-x", "data"),
)
def create_subreg_timeseries_data(subregion_df, reg_names, series_indicator_names):
    def apply_index_name(index):
        return reg_names.loc[index]["name"]

    def apply_indicator_name(index):
        return series_indicator_names.loc[index]["name"]

    subregion_df.index = subregion_df.index.map(apply_index_name)
    subregion_df.dimensions = subregion_df.dimensions.map(apply_indicator_name)
    
    return Serverside(subregion_df)


@callback(
    Output("key-figures-finland-series-data-municipality-en", "data"),
    Input("key-figures-finland-series-data-municipality-x", "data"),
    State("key-figures-finland-region-names-x", "data"),
    State("key-figures-finland-series-indicator-names-x", "data"),
)
def create_local_timeseries_data(mun_df, reg_names, series_indicator_names):
    def apply_index_name(index):
        return reg_names.loc[index]["name"]

    def apply_indicator_name(index):
        return series_indicator_names.loc[index]["name"]

    mun_df.index = mun_df.index.map(apply_index_name)
    mun_df.dimensions = mun_df.dimensions.map(apply_indicator_name)

    return Serverside(mun_df)


@callback(
    Output("key-figures-finland-timeseries-en", "figure"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
    Input("key-figures-finland-region-map-en", "hoverData"),
    Input("key-figures-finland-region-map-en", "clickData"),
    Input("key-figures-finland-region-map-en", "selectedData"),
    Input("key-figures-finland-chart-selection-en", "value"),
    Input(
        ThemeChangerAIO.ids.radio("key-figures-finland-key-theme-selection-x"), "value"
    ),
    Input("key-figures-finland-chart-template-en", "value"),
    State("key-figures-finland-region-selection-en", "value"),
    Input("key-figures-finland-series-data-region-en", "data"),
    Input("key-figures-finland-series-data-subregion-en", "data"),
    Input("key-figures-finland-series-data-municipality-en", "data"),
)
def update_timeseries_chart(
    key_figure,
    hov_data,
    click_data,
    sel_data,
    chart_type,
    theme,
    template,
    region,
    region_df,
    subregion_df,
    mun_df,
):
    if region_df is None or subregion_df is None or mun_df is None:
        raise PreventUpdate

    kf = ", ".join(key_figure.split(", ")[:-1])

    if region == "Municipality":
        if mun_df is None:
            raise PreventUpdate
        dff = mun_df
    elif region == "Sub-region":
        if subregion_df is None:
            raise PreventUpdate
        dff = subregion_df
        #dff.index = [c if c == 'WHOLE COUNTRY' else ' '.join(c.split()[1:]).strip() for c in dff.index]
    else:
        if region_df is None:
            raise PreventUpdate
        dff = region_df
        #dff.index = [c if c == 'WHOLE COUNTRY' else ' '.join(c.split()[1:]).strip() for c in dff.index]

    if sel_data is not None:

        location = sorted([point["location"] for point in sel_data["points"]])

    elif click_data is not None:

        location = [click_data["points"][0]["location"]]

    elif hov_data is not None:

        location = [hov_data["points"][0]["location"]]

    else:

        location = ["WHOLE COUNTRY"]

   
    try:
        dff = dff.loc[location].query(f"dimensions=='{kf}'")

    except:
        dff = region_df.loc[location].query(f"dimensions=='{kf}'")

    loc_string = {
        True: (f": {location[0]}").replace(": WHOLE COUNTRY", " Finland"),
        False: f" selected {region}s".replace("ty", "ties")
        .replace("Muni", "muni")
        .replace("Region", "region")
        .replace("Sub-r", "sub-r"),
    }[len(location) == 1]
    template = template_from_url(theme) if template == "bootstrap_theme" else template

    name = dff["dimensions"].values[0]
    dff = dff.reset_index().rename(columns={"value": name, "Region": region})
    dff.Year = dff.Year.astype(int)
    dff[region] = dff[region].astype(str)

    if chart_type == "line":
        fig = px.line(
            dff,
            x="Year",
            y=name,
            color=region,
            template=template,
            hover_data=[region, "Year", name],
            title=f"{kf} per year in<b>{loc_string}<b>",
        )
        fig.update_traces(line=dict(width=4))
    else:
        fig = px.area(
            dff,
            x="Year",
            y=name,
            color=region,
            template=template,
            hover_data=[region, "Year", name],
            title=f"{kf} per year in<b>{loc_string}<b>",
        )
    fig.update_layout(margin=dict(l=0, r=0), hoverlabel=dict(font_size=23))

    return fig


@callback(
    Output("key-figures-finland-header-en", "children"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
    Input("key-figures-finland-region-selection-en", "value"),
)
def update_header(key_figure, region_level):
    return f"{key_figure} by {region_level}".capitalize()


@callback(
    Output("key-figures-finland-whole-country-header-en", "children"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
)
def update_whole_country_header(key_figure):

    # Get all the header components.
    dff = whole_country_df.loc[key_figure]
    stat_name = dff.stat_name
    stat_unit = dff.unit
    stat_year = dff["year"]
    stat_value = dff["WHOLE COUNTRY"]

    # Change values with no decimals (.0) to int.
    stat_value = {True: int(stat_value), False: stat_value}[".0" in str(stat_value)]
    # Use space as thousand separator.
    stat_value = "{:,}".format(stat_value)

    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [stat_name, ", ", stat_year, " in Finland:"],
                                        className="card-title text-primary display-3",
                                    )
                                ]
                            )
                        ],
                        sm=12,
                        md=12,
                        lg=7,
                        xl=7,
                        xxl=7,
                    ),
                    dbc.Col(
                        [
                            dbc.CardBody(
                                [
                                    html.Span(
                                        [stat_value, " ", stat_unit],
                                        className="card-text text-info display-2",
                                    )
                                ]
                            )
                        ],
                        sm=12,
                        md=12,
                        lg=5,
                        xl=5,
                        xxl=5,
                        align="center",
                    ),
                ]
            )
        ],
        className="border",
    )


@callback(
    Output("key-figures-finland-geojson-data-en", "data"),
    Input("key-figures-finland-region-selection-en", "value"),
    State("key-figures-finland-geojson-collection-x", "data"),
    prevent_initial_call=True
)
def store_geojson(region, geojson_collection):
    
    return geojson_collection[region]


@callback(
    Output("key-figures-finland-region-map-en", "selectedData"),
    Output("key-figures-finland-region-map-en", "clickData"),
    Input("key-figures-finland-region-selection-en", "value"),
    Input("key-figures-finland-key-figure-selection-en", "value")
)
def reset_map_selections(kf, reg):
    return None, None


@callback(
    Output("key-figures-finland-locations-en", "data"),
    Output("key-figures-finland-zs-en", "data"),
    Input("key-figures-finland-key-figure-selection-en", "value"),
    Input("key-figures-finland-region-selection-en", "value"),
)
def store_data(key_figure, region):
   
    dff = data_df.loc[region][["name", key_figure]]

    return dff["name"].values, dff[key_figure].values


clientside_callback(
    """
    function(geojson, locations, z, map_type, colorscale){           
       
        console.log("Updating map with data:", geojson, locations, z);
        var layout = {
            'height':600,
            'mapbox': {'style':map_type,'zoom':3.8,'center':{'lat': 64.961093, 'lon': 25.795386}
            },
            'margin':{'l':0,'t':0,'b':0,'r':0}
        };
        var data = [{            
            'type':'choroplethmapbox',            
            'name':'',
            'geojson':geojson,
            'locations':locations,
            'featureidkey':'properties.name',
            'hovertemplate': '<b>%{location}</b><br>%{z:,}',
            'hoverlabel':{'font':{'family':'Arial Black', 'size':20, 'color':'black'},'bgcolor':'white'},
            'z':z,
            'colorscale':colorscale
        }];

        return {'data':data,'layout':layout}
    }   

""",
    Output("key-figures-finland-region-map-en", "figure"),
    Input("key-figures-finland-geojson-data-en", "data"),
    Input("key-figures-finland-locations-en", "data"),
    Input("key-figures-finland-zs-en", "data"),
    Input("key-figures-finland-map-type-en", "value"),
    Input("key-figures-finland-map-colorscale-en", "value")
)
