# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:23:29 2022

@author: tuomas.poukkula
"""

from dash_extensions.enrich import DashProxy, Input, Output, ServersideOutput, ServersideOutputTransform, State, html, dcc, page_container, callback, callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO
from dash_iconify import DashIconify
import orjson
import requests
import pandas as pd
import numpy as np


# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:kunta1000k_2021&outputFormat=json
with open('assets/municipalities_multilang.json', encoding = 'utf-8') as f:
    municipalities_json = orjson.loads(f.read())
    
# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=maakunta1000k_2021&outputFormat=json
with open('assets/regions_multilang.json', encoding = 'utf-8') as f:
    regions_json = orjson.loads(f.read())

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:seutukunta1000k_2021&outputFormat=json    
with open('assets/subregions_multilang.json', encoding = 'utf-8') as f:
    subregions_json = orjson.loads(f.read())
    
geojson_collection = {'Municipality':municipalities_json, 'Region':regions_json,'Sub-region': subregions_json}

def get_region_names():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    df = None
    for lang in ['fi','sv','en']:
        url = f"https://pxdata.stat.fi:443/PxWeb/api/v1/{lang}/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_viimeisin.px"
        json = requests.get(url, headers=headers).json()
        dff = pd.DataFrame([{'id':i, {'fi':'nimi','sv':'namn','en':'name'}[lang]:name} for i,name in zip(json['variables'][0]['values'],json['variables'][0]['valueTexts'])])
        if df is None:
            df = dff
        else:
            df = pd.merge(left = df, right = dff, on = 'id', how = 'inner')
    df = df.astype({'id':'category','nimi':'category', 'namn':'category', 'name':'category'})
    return df.set_index('id')

def get_series_indicator_names():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    df = None
    for lang in ['fi','sv','en']:
        url = f"https://pxdata.stat.fi:443/PxWeb/api/v1/{lang}/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_aikasarja.px"
        json = requests.get(url, headers=headers).json()
        dff = pd.DataFrame([{'id':i, {'fi':'nimi','sv':'namn','en':'name'}[lang]:name} for i,name in zip(json['variables'][1]['values'],json['variables'][1]['valueTexts'])])
        if df is None:
            df = dff
        else:
            df = pd.merge(left = df, right = dff, on = 'id', how = 'inner')
    df = df.astype({'id':'category','nimi':'category', 'namn':'category', 'name':'category'})
    return df.set_index('id')

def get_timeseries_data(region_level, split = 3):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    
    with open(f'./assets/{region_level}_series_payload.json') as f:
        payload = orjson.loads(f.read())
    
    series_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_aikasarja.px"
    
    if region_level == 'Municipality':
        
        year_lists = np.array_split([str(c) for c in requests.get(series_url, headers = headers).json()['variables'][-1]['values']], split)
        
        dfs = []
        
        for year_list in year_lists:
            payload['query'][-1]['selection'] = {'filter': 'item', 'values': list(year_list)}
            
            json = requests.post(series_url, json = payload, headers = headers).json()
            cities = list(json['dimension']['Alue 2021']['category']['label'].keys())
    
            dimensions = list(json['dimension']['Tiedot']['category']['label'].keys())
            years = list(json['dimension']['Vuosi']['category']['label'].values())
            
            values = json['value']

            cities_df = pd.DataFrame(cities, columns = ['Region'])
            cities_df['Region'] = cities_df['Region'].astype('category')
            cities_df['index'] = 0
            dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
            dimensions_df['dimensions'] = dimensions_df['dimensions'].astype('category')
            dimensions_df['index'] = 0
            years_df = pd.DataFrame(years, columns = ['Year'])
            years_df['Year'] = years_df['Year'].astype('category')
            years_df['index'] = 0

            data = pd.merge(left = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer'),
                            right = years_df, how = 'outer', on = 'index').drop('index',axis = 1)

            data['value'] = values
            dfs.append(data.set_index('Region'))
        data = pd.concat(dfs)
        data.dropna(axis=0,inplace=True)
        return data

        
    else:
    
        json = requests.post(series_url, json = payload, headers = headers).json()
        


        cities = list(json['dimension']['Alue 2021']['category']['label'].keys())

        dimensions = list(json['dimension']['Tiedot']['category']['label'].keys())
        years = list(json['dimension']['Vuosi']['category']['label'].values())



        values = json['value']

        cities_df = pd.DataFrame(cities, columns = ['Region'])
        cities_df['Region'] = cities_df['Region'].astype('category')
        cities_df['index'] = 0
        dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
        dimensions_df['dimensions'] = dimensions_df['dimensions'].astype('category')
        dimensions_df['index'] = 0
        years_df = pd.DataFrame(years, columns = ['Year'])
        years_df['Year'] = years_df['Year'].astype('category')
        years_df['index'] = 0

        data = pd.merge(left = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer'),
                        right = years_df, how = 'outer', on = 'index').drop('index',axis = 1)

        data['value'] = values
        data.dropna(axis=0,inplace=True)
    
        return data.set_index('Region')
    
timeseries_region = get_timeseries_data('Region')
timeseries_subregion = get_timeseries_data('Sub-region')
timeseries_municipality = get_timeseries_data('Municipality')

series_indicator_names= get_series_indicator_names()
reg_names = get_region_names()    



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

footer = dbc.Card(id ='key-figures-finland-footer-x', children= [
        
        dbc.Row([
            
            dbc.Col(dbc.NavLink(DashIconify(icon="logos:github"), href="https://github.com/tuopouk/key_figures_in_finland",external_link=True, target='_blank',className="btn btn-link btn-floating btn-lg text-dark m-1"),className="mb-4" ,xl=1,lg=1,md=4,sm=4,xs=4),
            dbc.Col(dbc.NavLink(DashIconify(icon="logos:twitter"), href="https://twitter.com/TuomasPoukkula",external_link=True, target='_blank',className="btn btn-link btn-floating btn-lg text-dark m-1"),className="mb-4",xl=1,lg=1,md=4,sm=4,xs=4   ),
            dbc.Col(dbc.NavLink(DashIconify(icon="logos:linkedin"), href="https://www.linkedin.com/in/tuomaspoukkula/",external_link=True, target='_blank',className="btn btn-link btn-floating btn-lg text-dark m-1"),className="mb-4",xl=1,lg=1,md=4,sm=4,xs=4  )
            
            
            
            ],className ="d-flex justify-content-center align-items-center", justify='center',align='center')
    
    
    ],className ='card text-white bg-secondary mt-3 navbar-static-top')

navbar = dbc.Navbar(
    
    dbc.Container([
    
        dbc.Row([
            
            dbc.Col([
                html.A([
                    html.Img(src = 'assets/gofore_logo_white.svg',
                              height="60px")
                    ],
                    href = 'https://gofore.com/', 
                    target='_blank')
                ]),#xl = 4, lg = 4, md = 12, sm = 12),
       
            dbc.Col([
                dbc.NavItem(change_theme),
                
                ], align='center')
    
            
            ],
            className = "d-flex justify-content-start"
            ),
        
    
        dbc.Row([
                        dbc.Col(
                            [
                             
                               dbc.Collapse(
                                dbc.Nav([
                                    
                                    dbc.NavbarBrand("by: Tuomas Poukkula",style={'font-style':'italic'}, className="ms-2"),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-github"), href="https://github.com/tuopouk/key_figures_in_finland",external_link=True, target='_blank') ),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi bi-twitter"), href="https://twitter.com/TuomasPoukkula",external_link=True, target='_blank') ),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-linkedin"), href="https://www.linkedin.com/in/tuomaspoukkula/",external_link=True, target='_blank') ),
                                    dbc.NavItem(id = 'key-figures-finland-email-x',children = [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Key Figures Finland",external_link=True, target='_blank')] ),
                                    
                                ]
                                ),
                                 id="key-figures-finland-navbar-collapse-x",
                                 is_open=False,
                                 navbar=True
                               )
                              ]
                        )
                    ], className = "d-flex justify-content-end"),
            
            dbc.Row([
                dbc.Col([dbc.DropdownMenu(id ='key-figures-finland-dd_menu-x',
                                          # size="lg",
                                          # menu_variant="dark",
                                          children =
                                                [
                                                    dbc.DropdownMenuItem('EN',id = 'en',  href='/'),
                                                    dbc.DropdownMenuItem('FI',id = 'fi',  href='/fi'),
                                                      dbc.DropdownMenuItem('SV',id = 'sv',  href='/sv')
                                                ],
                    # nav=True,
                    label="文 / A"
                )], align = 'center')
                
                  ], align = 'center', className = "d-flex justify-content-end"),
    
        
          ],className='d-flex justify-content-between', fluid=True),
                                
        color="primary",
        dark=True,
        className = 'navbar navbar-default navbar-static-top mb-5'
    )

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

external_stylesheets = [dbc.themes.LUX,
                        dbc.icons.BOOTSTRAP,
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                        dbc_css]
external_scripts = ["https://cdn.plot.ly/plotly-locale-fi-latest.js",
                    "https://cdn.plot.ly/plotly-locale-sv-latest.js"]

app = DashProxy(name = __name__, 
                transforms = [ServersideOutputTransform()],
           external_stylesheets = external_stylesheets,
           external_scripts = external_scripts,
           use_pages = True
           )


# Stuff for PWA.
app.index_string = '''<!DOCTYPE html>
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
'''


app.layout = dbc.Container([
                dcc.Location(id='key-figures-finland-location-x'),
                dcc.Store(id = 'key-figures-finland-geojson-collection-x'),
                dcc.Store(id = 'key-figures-finland-region-names-x'),
                dcc.Store(id = 'key-figures-finland-series-indicator-names-x'),
                dcc.Store(id = 'key-figures-finland-series-data-region-x'),
                dcc.Store(id = 'key-figures-finland-series-data-subregion-x'),
                dcc.Store(id = 'key-figures-finland-series-data-municipality-x'),
                navbar,
                page_container,
                footer
    
    ], fluid = True, className = 'dbc')

# Do stuff to make the data be stored on the server
@callback(    
    ServersideOutput('key-figures-finland-geojson-collection-x', 'data'),Input('key-figures-finland-footer-x', 'id')
    )
def update_geojson_collection(gimmick):
    return geojson_collection


@callback(    
    ServersideOutput('key-figures-finland-region-names-x', 'data'),Input('key-figures-finland-footer-x', 'id')
    )
def update_region_names(gimmick):
    return reg_names

@callback(    
    ServersideOutput('key-figures-finland-series-indicator-names-x', 'data'),Input('key-figures-finland-footer-x', 'id')
   )
def update_indicator_names(gimmick):
    return series_indicator_names

@callback(    
    ServersideOutput('key-figures-finland-series-data-region-x', 'data'),Input('key-figures-finland-footer-x', 'id')
    )
def update_region_series(gimmick):
    return timeseries_region

@callback(    
    ServersideOutput('key-figures-finland-series-data-subregion-x', 'data'),Input('key-figures-finland-footer-x', 'id')
    )
def update_region_series(gimmick):
    return timeseries_subregion

@callback(    
    ServersideOutput('key-figures-finland-series-data-municipality-x', 'data'),Input('key-figures-finland-footer-x', 'id')
    )
def update_region_series(gimmick):
    return timeseries_municipality    
    
    


@callback(
    Output('key-figures-finland-dd_menu-x','label'), 
    Input('fi','n_clicks'),Input('en','n_clicks'),Input('sv','n_clicks')

)
def update_label(*args):
    
    ctx = callback_context

    if not ctx.triggered:
        # button_id = "fi"
        return '文 / A'
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == 'fi':
        return 'FI'
    elif button_id == 'en':
        return 'EN'
    else:
        return 'SV'
    
@callback(
    Output('key-figures-finland-email-x','children'),
    Input('key-figures-finland-location-x','pathname')
    
    )
def update_email_topic(label):
        

    if label == '/':
        return [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Suomen alueelliset avainluvut",external_link=True, target='_blank')]
    elif label == '/en':
        return [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Key Figures Finland",external_link=True, target='_blank')]
    elif label == '/sv':
        return [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Finlands regionala nyckeltal",external_link=True, target='_blank')]
    else:
       return [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Key Figures Finland",external_link=True, target='_blank')] 

@callback(

      Output(ThemeChangerAIO.ids.button("key-figures-finland-key-theme-selection-x"), "title"),
      Output(ThemeChangerAIO.ids.button("key-figures-finland-key-theme-selection-x"), "children"),
      Output(ThemeChangerAIO.ids.offcanvas("key-figures-finland-key-theme-selection-x"), "title"),
      Input('key-figures-finland-location-x','pathname')
    
)
def change_theme_changer_language(pathname):
    
    if pathname == '/':
        return 'Vaihda väriteemaa', 'Vaihda väriteemaa', "Valitse jokin alla olevista väriteemoista"
    elif pathname == '/en':
        return 'Change Color Theme', 'Change Color Theme', "Select a Color Theme"
    elif pathname == '/sv':
        return "Ändra färgtema", "Ändra färgtema", "Välj ett färgtema"
    else:
        return 'Vaihda väriteemaa', 'Vaihda väriteemaa', "Valitse jokin alla olevista väriteemoista"

server = app.server
if __name__ == '__main__':
	app.run_server(debug=False)