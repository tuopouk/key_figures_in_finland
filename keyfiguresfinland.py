# -*- coding: utf-8 -*-
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import orjson
import random
from plotly.io.json import to_json_plotly

municipal_data = pd.read_csv('assets/key_figures_municipalities.csv', encoding = 'latin-1').rename(columns ={'Region 2021':'Municipality'}).set_index('Municipality')
regions_data = pd.read_csv('assets/key_figures_regions.csv', encoding = 'latin-1').rename(columns ={'Region 2021':'Region'}).set_index('Region')
subregions_data = pd.read_csv('assets/key_figures_subregions.csv', encoding = 'latin-1').rename(columns ={'Region 2021':'Sub-region'}).set_index('Sub-region')
whole_country_df = municipal_data.loc['WHOLE COUNTRY']

# The municipal dataset also has the whole country's key figures.
municipal_data.drop('WHOLE COUNTRY', axis = 0, inplace = True)

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:kunta1000k_2021&outputFormat=json
with open('assets/municipalities.json', encoding = 'ISO-8859-1') as f:
    municipalities_json = orjson.loads(f.read())
    
# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=maakunta1000k_2021&outputFormat=json
with open('assets/regions.json', encoding = 'ISO-8859-1') as f:
    regions_json = orjson.loads(f.read())

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:seutukunta1000k_2021&outputFormat=json    
with open('assets/sub-regions.json', encoding = 'utf-8') as f:
    subregions_json = orjson.loads(f.read())
    
geojson_collection = {'Municipality':municipalities_json, 'Region':regions_json, 'Sub-region': subregions_json}
data_collection =  {'Municipality':municipal_data, 'Region':regions_data, 'Sub-region': subregions_data}

key_figures = sorted(list(pd.unique(municipal_data.columns)))

external_stylesheets = [dbc.themes.SUPERHERO]

app = Dash(name = __name__, external_stylesheets = external_stylesheets
          )
app.title = "Finland's Municipal Key Figures"
server = app.server

def serve_layout():
    
    return dbc.Container([
        
        html.Div("Finland's Municipal Key Figures",style={'textAlign':'center'}, className="mb-3 mt-3 fw-bold display-1"),

        dbc.Row([
            
            dbc.Col([
                html.H2('Key figure'),
                dcc.Dropdown(id = 'key-figures-finland-key-figure-selection-x',
                             options = key_figures,
                             value = "Degree of urbanisation, %, 2020",
                             multi = False,
                             style = {'font-size':20, 'font-family':'Arial','color': 'black'}
                             ),
                html.Br(),
                html.H2('Regional level'),
                dcc.Dropdown(id = 'key-figures-finland-region-selection-x',
                             options = [{'label':region, 'value':region} for region in data_collection.keys()],
                             value = 'Municipality',
                             multi = False,
                             style = {'font-size':20, 'font-family':'Arial','color': 'black'}
                             ),
                html.H1(id = 'key-figures-finland-whole-country-header-x', style = {'textAlign':'center'}, className="mt-5 display-2"),
                html.Div(['Data by ',html.A('Statistics Finland', href = 'https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/kuntien_avainluvut_2021_viimeisin.px/', target = '_blank')], className="text-center fs-3 text"),
                
                ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, align = 'center'),
            dbc.Col([
                html.H1(id = 'key-figures-finland-header-x', style = {'textAlign':'center'}, className="mb-3 mt-3 display-3"),
                dcc.Loading(type = random.choice(['graph', 'cube', 'circle', 'dot' ,'default']), children =dcc.Graph(id = 'key-figures-finland-region-map-x', figure = plot_empty_map()))
                
                ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6)

            ], justify = 'center', className = "m-auto d-flex justify-content-center"),
        dcc.Store(id = 'key-figures-finland-map-data-store-x'),
        dcc.Store(id = 'key-figures-finland-map-layout-store-x')        
        ], fluid = True)    

def plot_empty_map():
    return px.choropleth_mapbox(center = {"lat": 64.961093, "lon": 27.590605})

def plot_map(key_figure, region_level):
    
    df = data_collection[region_level]
    geojson = geojson_collection[region_level]
    
    fig = px.choropleth_mapbox(df[[key_figure]].reset_index(), 
                           geojson=geojson, 
                           locations=region_level, 
                           color=key_figure,
                           mapbox_style="open-street-map",
                           featureidkey='properties.name',
                           zoom=4.2, 
                           color_continuous_scale = 'viridis',
                           center = {"lat": 64.961093, "lon": 27.590605},                           
                           labels={key_figure: key_figure}
                      )
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      height=800,
                      hoverlabel = dict(font_size = 28, font_family = 'Arial')
                      )    
    return fig

@app.callback(Output('key-figures-finland-header-x','children'),Input('key-figures-finland-key-figure-selection-x', 'value'),Input('key-figures-finland-region-selection-x', 'value') )
def update_header(key_figure, region_level):
    return f"{key_figure} by {region_level}".capitalize()

@app.callback(Output('key-figures-finland-whole-country-header-x','children'),Input('key-figures-finland-key-figure-selection-x', 'value'))
def update_whole_country_header(key_figure):
    kf_string = key_figure.split(',')
    kf_string.pop(-2)
    kf_string = ', '.join(kf_string)
    kf_string = {True:key_figure, False:kf_string}[len(kf_string.split(','))==1]
    return html.P([kf_string,html.Br(),"in Finland:",html.Br(), ("{:,}".format(whole_country_df.loc[key_figure])).replace('.0','').replace(',',' ')+key_figure.split(',')[-2].replace('2020','').replace('2021','').replace(key_figure.split(',')[0],'')],className="fw-bold")

@app.callback(
    Output('key-figures-finland-map-data-store-x','data'),
    Output('key-figures-finland-map-layout-store-x','data'),
    Input('key-figures-finland-key-figure-selection-x', 'value'),
    Input('key-figures-finland-region-selection-x', 'value')       
)
def update_map(key_figure, region_level):
    
    map_figure = plot_map(key_figure, region_level)        
    map_data = orjson.loads(to_json_plotly(map_figure))['data']
    map_layout = orjson.loads(to_json_plotly(map_figure))['layout']
    
    return map_data, map_layout    
   
app.clientside_callback(

    """
    function(data, layout){    
        return {
            'data':data,
            'layout':layout
        }
    }    
    
    """,
    Output('key-figures-finland-region-map-x', 'figure'),
    [Input('key-figures-finland-map-data-store-x','data'),
    Input('key-figures-finland-map-layout-store-x','data')]
)
app.layout = serve_layout
if __name__ == "__main__":
    app.run_server(debug=True)    
