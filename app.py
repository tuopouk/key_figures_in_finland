# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:23:29 2022

@author: tuomas.poukkula
"""

from dash_extensions.enrich import (
    DashProxy,
    Input,
    Output,
    Serverside,
    ServersideOutputTransform,
    html,
    dcc,
    page_container,
    callback,
    callback_context,
)
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash_iconify import DashIconify
import orjson
import requests
import pandas as pd
import numpy as np
# import geopandas as gpd
import json
import time
import os



from cachelib.file import FileSystemCache

# configure cache directory
cache = FileSystemCache(cache_dir="C:/temp/mycache", threshold=500, default_timeout=300)

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:kunta1000k_2023&outputFormat=json
with open("assets/municipalities_multilang.json", encoding="utf-8") as f:
    municipalities_json = json.loads(f.read())

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=maakunta1000k_2023&outputFormat=json
with open("assets/regions_multilang.json", encoding="utf-8") as f:
    regions_json = json.loads(f.read())


# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:seutukunta1000k_2023&outputFormat=json
with open("assets/subregions_multilang.json", encoding="utf-8") as f:
    subregions_json = json.loads(f.read())

geojson_collection = {
    "Municipality": municipalities_json,
    "Region": regions_json,
    "Sub-region": subregions_json,
}



# Helpers
def safe_post(url, payload, headers, retries=5, delay=5):
    for attempt in range(retries):
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            wait = delay * (attempt + 1)
            print(f"Rate limited, waiting {wait}s...")
            time.sleep(wait)
        else:
            resp.raise_for_status()
    raise RuntimeError("Failed after retries")

def fetch_meta_cached(url, headers, region_level):
    cache_file = f"./assets/{region_level}_meta.json"
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return orjson.loads(f.read())
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    meta = resp.json()
    with open(cache_file, "wb") as f:
        f.write(orjson.dumps(meta))
    return meta

def load_or_fetch_timeseries(region_level, cache_file):
    if os.path.exists(cache_file):
        return pd.read_pickle(cache_file)
    df = get_timeseries_data(region_level)
    df.to_pickle(cache_file)
    return df



def get_region_names():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }
    df = None
    for lang in ["fi", "sv", "en"]:
        url = f"https://pxdata.stat.fi:443/PxWeb/api/v1/{lang}/Kuntien_avainluvut/uusin/kuntien_avainluvut_viimeisin.px"
        resp = requests.get(url, headers=headers)
        meta = resp.json()
        if "variables" not in meta:
            print("API error:", meta)
            continue
        dff = pd.DataFrame(
            [
                {"id": i, {"fi": "nimi", "sv": "namn", "en": "name"}[lang]: name}
                for i, name in zip(meta["variables"][0]["values"], meta["variables"][0]["valueTexts"])
            ]
        )
        df = dff if df is None else pd.merge(df, dff, on="id", how="inner")

    if df is None:
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=["id", "nimi", "namn", "name"]).set_index("id")

    df = df.astype({"id": "category", "nimi": "category", "namn": "category", "name": "category"})
    # Clean names
    df.nimi = [c if c == "KOKO MAA" or (c[:2] not in ["SK", "MK"]) else " ".join(c.split()[1:]).strip() for c in df.nimi]
    df.name = [c if c == "WHOLE COUNTRY" or (c[:2] not in ["SK", "MK"]) else " ".join(c.split()[1:]).strip() for c in df.name]
    df.namn = [c if c == "HELA LANDET" or (c[:2] not in ["SK", "MK"]) else " ".join(c.split()[1:]).strip() for c in df.namn]

    return df.set_index("id")




def get_series_indicator_names():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }
    df = None
    for lang in ["fi", "sv", "en"]:
        url = f"https://pxdata.stat.fi:443/PxWeb/api/v1/{lang}/Kuntien_avainluvut/uusin/kuntien_avainluvut_aikasarja.px"
        resp = requests.get(url, headers=headers)
        meta = resp.json()
        if "variables" not in meta:
            print("API error:", meta)
            continue
        dff = pd.DataFrame(
            [
                {"id": i, {"fi": "nimi", "sv": "namn", "en": "name"}[lang]: name}
                for i, name in zip(
                    meta["variables"][1]["values"], meta["variables"][1]["valueTexts"]
                )
            ]
        )
        df = dff if df is None else pd.merge(df, dff, on="id", how="inner")

    if df is None:
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=["id", "nimi", "namn", "name"]).set_index("id")

    # Ensure all expected columns exist, even if empty
    for col in ["nimi", "namn", "name"]:
        if col not in df.columns:
            df[col] = pd.Series(dtype="string")

    # Cast only existing columns
    dtype_map = {"id": "category", "nimi": "category", "namn": "category", "name": "category"}
    existing_map = {col: dtype for col, dtype in dtype_map.items() if col in df.columns}
    df = df.astype(existing_map)

    return df.set_index("id")



def get_timeseries_data(region_level, split=10):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }
    with open(f"./assets/{region_level}_series_payload.json") as f:
        payload = orjson.loads(f.read())
    series_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/Kuntien_avainluvut/uusin/kuntien_avainluvut_aikasarja.px"
    meta = fetch_meta_cached(series_url, headers, region_level)
    if "variables" not in meta:
        print("Metadata error:", meta)
        return pd.DataFrame()
    if region_level == "Municipality":
        year_values = meta["variables"][-1]["values"]
        year_lists = np.array_split([str(c) for c in year_values], split)
        dfs = []
        for year_list in year_lists:
            payload["query"][-1]["selection"] = {"filter": "item", "values": list(year_list)}
            data = safe_post(series_url, payload, headers)
            if "dimension" not in data:
                print("Data error:", data)
                continue
            cities = list(data["dimension"]["Alue"]["category"]["label"].keys())
            dimensions = list(data["dimension"]["Tiedot"]["category"]["label"].keys())
            years = list(data["dimension"]["Vuosi"]["category"]["label"].values())
            values = data["value"]
            cities_df = pd.DataFrame(cities, columns=["Region"]).astype("category")
            dimensions_df = pd.DataFrame(dimensions, columns=["dimensions"]).astype("category")
            years_df = pd.DataFrame(years, columns=["Year"]).astype("category")
            cities_df["index"] = dimensions_df["index"] = years_df["index"] = 0
            data_df = pd.merge(pd.merge(cities_df, dimensions_df, on="index"), years_df, on="index").drop("index", axis=1)
            data_df["value"] = values
            dfs.append(data_df.set_index("Region"))
        if dfs:
            data = pd.concat(dfs)
            data.dropna(axis=0, inplace=True)
            return data
        return pd.DataFrame()


# timeseries_region = get_timeseries_data("Region")
# timeseries_subregion = get_timeseries_data("Sub-region")
# timeseries_municipality = get_timeseries_data("Municipality")
# Top-level loads with cache and error handling
try:
    timeseries_region = load_or_fetch_timeseries("Region", "./assets/region_timeseries.pkl")
except Exception as e:
    print("Failed to load region timeseries:", e)
    timeseries_region = pd.DataFrame()
try:
    timeseries_subregion = load_or_fetch_timeseries(
        "Sub-region", "./assets/subregion_timeseries.pkl"
    )
except Exception as e:
    print("Failed to load subregion timeseries:", e)
    timeseries_subregion = pd.DataFrame()
try:
    timeseries_municipality = load_or_fetch_timeseries(
        "Municipality", "./assets/municipality_timeseries.pkl"
    )
except Exception as e:
    print("Failed to load municipality timeseries:", e)
    timeseries_municipality = pd.DataFrame()

series_indicator_names = get_series_indicator_names()
reg_names = get_region_names()


# change_theme = ThemeChangerAIO(
#     aio_id="key-figures-finland-key-theme-selection-x",
#     radio_props={"value": dbc.themes.LUX},
#     button_props={
#         "size": "md",
#         "outline": False,
#         # "style": {"marginTop": ".5rem"},
#         "color": "success",
#     },
# )

# about = dbc.Modal(id = 'key-figures-finland-about-x')

footer = dbc.Card(
    id="key-figures-finland-footer-x",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavLink(
                        DashIconify(icon="logos:github"),
                        href="https://github.com/tuopouk/key_figures_in_finland",
                        external_link=True,
                        target="_blank",
                        className="btn btn-link btn-floating btn-lg text-dark m-1",
                    ),
                    className="mb-4",
                    xl=1,
                    lg=1,
                    md=4,
                    sm=4,
                    xs=4,
                ),
                dbc.Col(
                    dbc.NavLink(
                        DashIconify(icon="logos:twitter-x"),
                        href="https://twitter.com/TuomasPoukkula",
                        external_link=True,
                        target="_blank",
                        className="btn btn-link btn-floating btn-lg text-dark m-1",
                    ),
                    className="mb-4",
                    xl=1,
                    lg=1,
                    md=4,
                    sm=4,
                    xs=4,
                ),
                dbc.Col(
                    dbc.NavLink(
                        DashIconify(icon="logos:linkedin"),
                        href="https://www.linkedin.com/in/tuomaspoukkula/",
                        external_link=True,
                        target="_blank",
                        className="btn btn-link btn-floating btn-lg text-dark m-1",
                    ),
                    className="mb-4",
                    xl=1,
                    lg=1,
                    md=4,
                    sm=4,
                    xs=4,
                ),
            ],
            className="d-flex justify-content-center align-items-center",
            justify="center",
            align="center",
        )
    ],
    className="card text-white bg-secondary mt-3 navbar-static-top",
)



dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
)
# dbc_css = (
#     "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
# )

external_stylesheets = [
    dbc.themes.LUX,
    dbc.icons.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    dbc_css,
]
external_scripts = [
    "https://cdn.plot.ly/plotly-locale-fi-latest.js",
    "https://cdn.plot.ly/plotly-locale-sv-latest.js",
]

app = DashProxy(
    transforms=[ServersideOutputTransform()],
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    use_pages=True,
)
change_theme = ThemeChangerAIO(
    aio_id="key-figures-finland-key-theme-selection-x",
    radio_props={"value": dbc.themes.LUX},
    button_props={
        "size": "md",
        "outline": False,
        # "style": {"marginTop": ".5rem"},
        "color": "success",
    },
)

# Stuff for PWA.
app.index_string = """<!DOCTYPE html>
<html>
<head>
<title>Key Figures Finland</title>
<link rel="manifest" href="./assets/manifest.json" />
{%metas%}
{%favicon%}
{%css%}
</head>
<script type="module">
    import 'https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate';
    const el = document.createElement('pwa-update');
    document.body.appendChild(el);
</script>
<body>
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', ()=> {
      navigator
      .serviceWorker
      .register('./assets/sw01.js')
      .then(()=>console.log("Ready."))
      .catch(()=>console.log("Err..."));
    });
  }
</script>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    
                    dbc.Col(
                        [
                            dbc.NavItem(change_theme),
                        ],
                        align="center",
                    ),
                ],
                className="d-flex justify-content-start",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavbarBrand(
                                            "by: Tuomas Poukkula",
                                            style={"font-style": "italic"},
                                            className="ms-2",
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                html.I(className="bi bi-github"),
                                                href="https://github.com/tuopouk/key_figures_in_finland",
                                                external_link=True,
                                                target="_blank",
                                            )
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                html.I(className="bi bi bi-twitter-x"),
                                                href="https://twitter.com/TuomasPoukkula",
                                                external_link=True,
                                                target="_blank",
                                            )
                                        ),
                                        dbc.NavItem(
                                            dbc.NavLink(
                                                html.I(className="bi bi-linkedin"),
                                                href="https://www.linkedin.com/in/tuomaspoukkula/",
                                                external_link=True,
                                                target="_blank",
                                            )
                                        ),
                                 
                                    ]
                                ),
                                id="key-figures-finland-navbar-collapse-x",
                                is_open=False,
                                navbar=True,
                            )
                        ]
                    )
                ],
                className="d-flex justify-content-end",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.DropdownMenu(
                                id="key-figures-finland-dd-menu-x",
                                children=[
                                    dbc.DropdownMenuItem("EN", id="en", href="/"),
                                    dbc.DropdownMenuItem("FI", id="fi", href="/fi"),
                                    dbc.DropdownMenuItem("SV", id="sv", href="/sv"),
                                ],
                                # nav=True,
                                label="文 / A",
                            )
                        ],
                        align="center",
                    )
                ],
                align="center",
                className="d-flex justify-content-end",
            ),
        ],
        className="d-flex justify-content-between",
        fluid=True,
    ),
    color="primary",
    dark=True,
    className="navbar navbar-default navbar-static-top mb-5",
)

app.layout = dbc.Container(
    [
        dcc.Location(id="key-figures-finland-location-x"),
        dcc.Store(id="key-figures-finland-geojson-collection-x"),
        dcc.Store(id="key-figures-finland-region-names-x"),
        dcc.Store(id="key-figures-finland-series-indicator-names-x"),
        dcc.Store(id="key-figures-finland-series-data-region-x"),
        dcc.Store(id="key-figures-finland-series-data-subregion-x"),
        dcc.Store(id="key-figures-finland-series-data-municipality-x"),
        navbar,
        page_container,
        footer,
    ],
    fluid=True,
    className="dbc",
)

# Do stuff to make the data be stored on the server
@callback(
    Output("key-figures-finland-geojson-collection-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_geojson_collection(gimmick):
    return Serverside(geojson_collection)


@callback(
    Output("key-figures-finland-region-names-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_region_names(gimmick):
    return Serverside(reg_names)


@callback(
    Output("key-figures-finland-series-indicator-names-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_indicator_names(gimmick):
    return Serverside(series_indicator_names)


@callback(
    Output("key-figures-finland-series-data-region-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_region_series(gimmick):
    return Serverside(timeseries_region)


@callback(
    Output("key-figures-finland-series-data-subregion-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_subregion_series(gimmick):
    return Serverside(timeseries_subregion)


@callback(
    Output("key-figures-finland-series-data-municipality-x", "data"),
    Input("key-figures-finland-footer-x", "id"),
)
def update_mun_series(gimmick):
    return Serverside(timeseries_municipality)


@callback(
    Output("key-figures-finland-dd-menu-x", "label"),
    Input("fi", "n_clicks"),
    Input("en", "n_clicks"),
    Input("sv", "n_clicks"),
    prevent_initial_call=True
)
def update_label(*args):

    ctx = callback_context
    

    if not ctx.triggered:
        # button_id = "fi"
        return "文 / A"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "fi":
        return "FI"
    elif button_id == "en":
        return "EN"
    else:
        return "SV"



@callback(
    Output(
        ThemeChangerAIO.ids.button("key-figures-finland-key-theme-selection-x"), "title"
    ),
    Output(
        ThemeChangerAIO.ids.button("key-figures-finland-key-theme-selection-x"),
        "children",
    ),
    Output(
        ThemeChangerAIO.ids.offcanvas("key-figures-finland-key-theme-selection-x"),
        "title",
    ),
    Input("key-figures-finland-location-x", "pathname"),
)
def change_theme_changer_language(pathname):

    if pathname == "/fi":
        return (
            "Vaihda väriteemaa",
            "Vaihda väriteemaa",
            "Valitse jokin alla olevista väriteemoista",
        )
    elif pathname == "/":
        return "Change Color Theme", "Change Color Theme", "Select a Color Theme"
    elif pathname == "/sv":
        return "Ändra färgtema", "Ändra färgtema", "Välj ett färgtema"
    else:
        return "Change Color Theme", "Change Color Theme", "Select a Color Theme"


server = app.server
if __name__ == "__main__":
    app.run(debug=False)
