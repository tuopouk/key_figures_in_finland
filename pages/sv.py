# -*- coding: utf-8 -*-
import pandas as pd
from dash_extensions.enrich import dcc, html, Input, Output, State, ServersideOutput, register_page,callback, clientside_callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO
import plotly.express as px
import locale
import orjson
import requests
from dash.exceptions import PreventUpdate

try:
    locale.setlocale(locale.LC_ALL, 'sv_FI')
except:
    locale.setlocale(locale.LC_ALL, 'sv-FI')

register_page(__name__,
              title = "Finlands regionala nyckeltal",
              name = "Finlands regionala nyckeltal",
              description = "Visualisering av Finlands regionala nyckeltal",
              image = 'sv.png'
              )


config = {'locale':'sv'}

fig_df = pd.DataFrame([{'x':0, 'y':0, 'text':'Tidserier laddas...'}])
default_fig = px.scatter(fig_df, x='x',y='y',text='text')
default_fig.update_traces(mode='text',textfont_size=25)
default_fig.update_xaxes(showgrid=False, visible=False)
default_fig.update_yaxes(showgrid=False, visible=False)

def get_data(region_level):
    
    name = 'namn'
    
    # Query url
    url = "https://pxdata.stat.fi:443/PxWeb/api/v1/sv/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_viimeisin.px"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    
    with open(f'./assets/{region_level}_payload.json') as f:
        payload = orjson.loads(f.read())
    
    json = requests.post(url, json = payload, headers = headers).json()

    cities = list(json['dimension']['Alue 2021']['category']['label'].values())
    
    dimensions = list(json['dimension']['Tiedot']['category']['label'].values())

    values = json['value']

    cities_df = pd.DataFrame(cities, columns = [name])
    cities_df['index'] = 0
    dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
    dimensions_df['index'] = 0

    data = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer').drop('index',axis = 1)
    data['value'] = values
    data = pd.pivot_table(data, values = 'value', index = [name], columns = 'dimensions')
    data = data.reset_index()
    data['region_level'] = {'Region':'Landskap', 'Sub-region':'Ekonomisk region', 'Municipality': 'Kommun'}[region_level]
    data = data.set_index('region_level')
    data.index = data.index.astype('category')
    data[name] = data[name].astype('category')
    
    return data

data_df = pd.concat([get_data('Region'), get_data('Sub-region'), get_data('Municipality')]).drop_duplicates()
whole_country_df = pd.DataFrame(data_df.set_index('namn').loc['HELA LANDET'].sort_index())
whole_country_df['year'] = [stat.split(', ')[-1] for stat in whole_country_df.index]
whole_country_df['unit'] = [stat.split(', ')[-2] if len(stat.split(', ')) > 2 else '' for stat in whole_country_df.index]
whole_country_df['stat_name'] = [stat.split(', ')[0] if len(stat.split(', ')) < 4 else ', '.join(stat.split(', ')[:2]) for stat in whole_country_df.index]
data_df = data_df[data_df.namn != 'HELA LANDET']



layout = dbc.Container([
    
     
                
        html.H1("Finlands regionala nyckeltal", className = 'fw-bold display-1 text-center'),
        
        
            
            dbc.Row([
                
                
                dbc.Col([
                    
                    dbc.Card([
                        dbc.CardBody([
                    
                            dbc.Row([
                                
                                dbc.Col([
                                
                                    html.H2('Nyckeltal'),
                                    dcc.Dropdown(id = 'key-figures-finland-key-figure-selection-sv',
                                                 options = whole_country_df.index,
                                                 value = whole_country_df.index[0]
                                                 )
                                    ]),
                                dbc.Col([
                                    html.H2('Region nivå'),
                                    dcc.Dropdown(id = 'key-figures-finland-region-selection-sv',
                                                 options = ['Landskap','Ekonomisk region','Kommun'],
                                                 value = 'Landskap',
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    ])
                                ]),
                            html.Div(id = 'key-figures-finland-whole-country-header-sv', className="text-center card-title mt-5 mb-3"),
                            
                            dcc.Graph(id = 'key-figures-finland-timeseries-sv', className="border", figure = default_fig, config = config),
                            dcc.Loading([
                                dcc.Store(id = 'key-figures-finland-series-data-region-sv'),
                                dcc.Store(id = 'key-figures-finland-series-data-subregion-sv'),
                                dcc.Store(id = 'key-figures-finland-series-data-municipality-sv')
                                ]),
                            dbc.Row([
                            
                                dbc.Col([
                                    html.H3('Diagram', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-chart-selection-sv',
                                                 options = ['ytdiagram', 'linjediagram'],
                                                 value = 'linjediagram',
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    
                                    ]),
                                dbc.Col([
                                    
                                    html.H3('Diagrammall', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-chart-template-sv',
                                                 options = sorted([
                                                     "bootstrap tema",
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
                                                 ]),
                                                 value = "bootstrap tema",
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    
                                ]),
                            
                                
                            ]),
                            
                            
                            ]),
                         dbc.CardFooter(['Data källa ',html.A('Statistikcentralen', href = 'https://pxdata.stat.fi/PxWeb/pxweb/sv/Kuntien_avainluvut/Kuntien_avainluvut__2021/', target = '_blank')], className="text-center align-middle card-text fs-3 text mt-3")
                        
                        ], style = {'height':'100%'}),
                    
                    ], xs = 12, sm = 12, md = 6, lg = 6, xl = 6, xxl = 6, align = 'start'),
                dbc.Col([
                    
                    dbc.Card([
                        
                        dbc.CardBody([
                    
                            html.H1(id = 'key-figures-finland-header-sv', className="mb-3 mt-3 display-3 card-title text-center"),
                            dcc.Graph(id = 'key-figures-finland-region-map-sv',
                              figure = px.choropleth_mapbox(center = {"lat": 64.961093, "lon": 25.795386}), 
                              clear_on_unhover=True,
                              config = {'mapboxAccessToken':'pk.eyJ1IjoiZ3VkdW1hbyIsImEiOiJjanNrZzA5aWoyazU3NDN0Yjl6Y25zend6In0.zkMKSjHPzqG5mQCX-yWdMw',
                                        'locale':'sv'
                                        },
                              className = 'border'),
                    
                            dbc.Row([
                    
                                dbc.Col([
                                    html.H3('Karttyp', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-map-type-sv', 
                                                 options = sorted(["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" ,"stamen-watercolor"]),
                                                 value = "stamen-terrain",
                                                 className = 'text-dark bg-light text-nowrap')
                                    ]),
                                dbc.Col([
                                    html.H3('Färgskala', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-map-colorscale-sv', 
                                                 options = sorted(['Blackbody','Bluered','Blues','Cividis','Earth','Electric','Greens','Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds','Viridis','YlGnBu','YlOrRd']),
                                                 value = "RdBu",
                                                 className = 'text-dark bg-light text-nowrap')
                                    ]),
                                
                                ])
                            ]),
                         
                        ], style = {'height':'100%'})
                    
                    ], xs = 12, sm = 12, md = 6, lg = 6, xl = 6, xxl = 6)
    
                ], justify = 'center', className = "mt-3 d-flex justify-content-center"),
            
        
        dcc.Store(id = 'key-figures-finland-geojson-data-sv'),
        dcc.Store(id = 'key-figures-finland-locations-sv'),
        dcc.Store(id = 'key-figures-finland-zs-sv')
        
        


        ], fluid = True)    

@callback(

    ServersideOutput('key-figures-finland-series-data-region-sv','data'),
    Input('key-figures-finland-series-data-region-x','data'),
    State('key-figures-finland-region-names-x','data'),
    State('key-figures-finland-series-indicator-names-x','data')
)
def create_reg_timeseries_data(region_df, 
                                 reg_names, 
                                 series_indicator_names):

    
    def apply_index_name(index):
        return reg_names.loc[index]['namn']
    def apply_indicator_name(index):
        return series_indicator_names.loc[index]['namn']
    
    region_df.index = region_df.index.map(apply_index_name)
    region_df.dimensions = region_df.dimensions.map(apply_indicator_name)
    
    
    return region_df

@callback(

    ServersideOutput('key-figures-finland-series-data-subregion-sv','data'),
    Input('key-figures-finland-series-data-subregion-x','data'),
    State('key-figures-finland-region-names-x','data'),
    State('key-figures-finland-series-indicator-names-x','data')
)
def create_subreg_timeseries_data(subregion_df, 
                                 reg_names, 
                                 series_indicator_names):
    
    def apply_index_name(index):
        return reg_names.loc[index]['namn']
    def apply_indicator_name(index):
        return series_indicator_names.loc[index]['namn']
        
    subregion_df.index = subregion_df.index.map(apply_index_name)
    subregion_df.dimensions = subregion_df.dimensions.map(apply_indicator_name)
  
    
    return subregion_df

@callback(

    ServersideOutput('key-figures-finland-series-data-municipality-sv','data'),
    Input('key-figures-finland-series-data-municipality-x','data'),
    State('key-figures-finland-region-names-x','data'),
    State('key-figures-finland-series-indicator-names-x','data')
)
def create_local_timeseries_data(mun_df, 
                                 reg_names, 
                                 series_indicator_names):
    
    def apply_index_name(index):
        return reg_names.loc[index]['namn']
    def apply_indicator_name(index):
        return series_indicator_names.loc[index]['namn']
    
    mun_df.index = mun_df.index.map(apply_index_name)
    mun_df.dimensions = mun_df.dimensions.map(apply_indicator_name)
    
    return mun_df


@callback(


    Output('key-figures-finland-timeseries-sv','figure'),
    Input('key-figures-finland-key-figure-selection-sv', 'value'),
    Input('key-figures-finland-region-map-sv', 'hoverData'),
    Input('key-figures-finland-region-map-sv', 'clickData'),
    Input('key-figures-finland-region-map-sv', 'selectedData'),
    Input('key-figures-finland-chart-selection-sv','value'),
    Input(ThemeChangerAIO.ids.radio("key-figures-finland-key-theme-selection-x"), "value"),
    Input('key-figures-finland-chart-template-sv','value'),
    State('key-figures-finland-region-selection-sv','value'),
    Input('key-figures-finland-series-data-region-sv','data'),
    Input('key-figures-finland-series-data-subregion-sv','data'),
    Input('key-figures-finland-series-data-municipality-sv','data'),
    
    
)
def update_timeseries_chart(key_figure, 
                            hov_data,
                            click_data, 
                            sel_data,  
                            chart_type, 
                            theme, 
                            template, 
                            region, 
                            region_df,
                            subregion_df,
                            mun_df
                            ):
    
    if region_df is None or subregion_df is None or mun_df is None:
        raise PreventUpdate
    
    kf = ', '.join(key_figure.split(', ')[:-1])

    if region == 'Kommun':
        if mun_df is None:
            raise PreventUpdate
        dff = mun_df
    elif region == 'Ekonomisk region':
        if subregion_df is None:
            raise PreventUpdate
        dff = subregion_df
    else:
        if region_df is None:
            raise PreventUpdate
        dff = region_df
    
      
    if sel_data is not None:
        
        location = sorted([point['location'] for point in sel_data['points']])
    
        
    elif click_data is not None:
        
        location = [click_data['points'][0]['location']]
    
    elif hov_data is not None:
        
        location = [hov_data['points'][0]['location']]
     
    else:
        
        location = ['HELA LANDET']
        
    try:    
        dff = dff.loc[location].query(f"dimensions=='{kf}'")
    
    except:
        dff = region_df.loc[location].query(f"dimensions=='{kf}'")
    
    loc_string = {True:(f': {location[0]}').replace(': HELA LANDET',' i Finland'), False: f'utvalda {region}er'.lower()}[len(location)==1]
    template = template_from_url(theme) if template == "bootstrap tema" else template    

    name = dff['dimensions'].values[0]
    dff = dff.reset_index().rename(columns = {'value':name, 'Region':region, 'Year': 'År'})
    dff.År = dff.År.astype(int)
    dff[region] = dff[region].astype(str)
    
    if chart_type == 'linjediagram':    
        fig = px.line(dff, x = 'År', y = name, color = region, template = template, hover_data = [region,'År',name], title = f'{kf} per år i <b>{loc_string}<b>')
        fig.update_traces(line=dict(width=4))
    else:
        fig = px.area(dff, x = 'År', y = name, color = region, template = template, hover_data = [region,'År',name], title = f'{kf} per år i <b>{loc_string}<b>')
    fig.update_layout(margin = dict(l=0,r=0),
                      hoverlabel=dict(font_size=23)
    )
    
    
    return fig


@callback(Output('key-figures-finland-header-sv','children'),Input('key-figures-finland-key-figure-selection-sv', 'value'),Input('key-figures-finland-region-selection-sv', 'value') )
def update_header(key_figure, region_level):
    return f"{key_figure} i {region_level}er".capitalize()



@callback(Output('key-figures-finland-whole-country-header-sv','children'),
          Input('key-figures-finland-key-figure-selection-sv', 'value'))
def update_whole_country_header(key_figure):
    
    # Get all the header components.
    dff = whole_country_df.loc[key_figure]
    stat_name = dff.stat_name
    stat_unit = dff.unit
    stat_year = dff['year']
    stat_value = dff['HELA LANDET']
    
    # Change values with no decimals (.0) to int.
    stat_value = {True: int(stat_value), False: stat_value}['.0' in str(stat_value)]
    # Use space as thousand separator.
    stat_value = "{:,}".format(stat_value).replace(',',' ')
    
    return dbc.Card(
        [
            dbc.Row([
                dbc.Col([
                    dbc.CardBody([
                        html.Div([stat_name, ", ", stat_year, " i Finland:"], className="card-title text-primary display-3")
                        ])
                    ],sm = 12, md = 12, lg = 7, xl = 7, xxl = 7),
                dbc.Col([
                    dbc.CardBody([
                        html.Span([stat_value, " ", stat_unit], className="card-text text-info display-2")
                        ])
                    ],sm = 12, md = 12,lg = 5, xl = 5, xxl = 5, align = 'center')
                ])
        ], className = 'border'
    )

@callback(
    Output('key-figures-finland-geojson-data-sv','data'),
    Input('key-figures-finland-region-selection-sv','value'),
    State('key-figures-finland-geojson-collection-x','data')
)
def store_geojson(region, geojson_collection):        
    return geojson_collection[{'Kommun':'Municipality','Ekonomisk region':'Sub-region','Landskap':'Region'}[region]]


@callback(
    Output('key-figures-finland-region-map-sv', 'selectedData'),
    Output('key-figures-finland-region-map-sv', 'clickData'),
    Input('key-figures-finland-region-selection-sv','value'),
    Input('key-figures-finland-key-figure-selection-sv', 'value')
)
def reset_map_selections(kf, reg):        
    return None, None

@callback(

    Output('key-figures-finland-locations-sv','data'),
    Output('key-figures-finland-zs-sv','data'),
    Input('key-figures-finland-key-figure-selection-sv','value'),
    Input('key-figures-finland-region-selection-sv','value')
    
)
def store_data(key_figure,region):

    dff = data_df.loc[region][['namn', key_figure]]
    return list(dff['namn'].values), list(dff[key_figure].values)

clientside_callback(

"""
    function(geojson, locations, z, map_type, colorscale){           
       
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
            'featureidkey':'properties.namn',
            'hovertemplate': '<b>%{location}</b><br>%{z:,}',
            'hoverlabel':{'font':{'family':'Arial Black', 'size':20, 'color':'black'},'bgcolor':'white'},
            'z':z,
            'colorscale':colorscale
        }];

        return {'data':data,'layout':layout}
    }   

""",
Output('key-figures-finland-region-map-sv', 'figure'),
Input('key-figures-finland-geojson-data-sv','data'),
Input('key-figures-finland-locations-sv','data'),
Input('key-figures-finland-zs-sv','data'),
Input('key-figures-finland-map-type-sv', 'value'),
Input('key-figures-finland-map-colorscale-sv', 'value')     
)
