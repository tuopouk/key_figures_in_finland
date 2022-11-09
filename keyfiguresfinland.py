# -*- coding: utf-8 -*-
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import orjson
import requests

# Query url
url = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_viimeisin.px"

# Municipal query body
mun_payload = {
  "query": [
    {
      "code": "Alue 2021",
      "selection": {
        "filter": "item",
        "values": [
          "SSS",
          "020",
          "005",
          "009",
          "010",
          "016",
          "018",
          "019",
          "035",
          "043",
          "046",
          "047",
          "049",
          "050",
          "051",
          "052",
          "060",
          "061",
          "062",
          "065",
          "069",
          "071",
          "072",
          "074",
          "075",
          "076",
          "077",
          "078",
          "079",
          "081",
          "082",
          "086",
          "111",
          "090",
          "091",
          "097",
          "098",
          "102",
          "103",
          "105",
          "106",
          "108",
          "109",
          "139",
          "140",
          "142",
          "143",
          "145",
          "146",
          "153",
          "148",
          "149",
          "151",
          "152",
          "165",
          "167",
          "169",
          "170",
          "171",
          "172",
          "176",
          "177",
          "178",
          "179",
          "181",
          "182",
          "186",
          "202",
          "204",
          "205",
          "208",
          "211",
          "213",
          "214",
          "216",
          "217",
          "218",
          "224",
          "226",
          "230",
          "231",
          "232",
          "233",
          "235",
          "236",
          "239",
          "240",
          "320",
          "241",
          "322",
          "244",
          "245",
          "249",
          "250",
          "256",
          "257",
          "260",
          "261",
          "263",
          "265",
          "271",
          "272",
          "273",
          "275",
          "276",
          "280",
          "284",
          "285",
          "286",
          "287",
          "288",
          "290",
          "291",
          "295",
          "297",
          "300",
          "301",
          "304",
          "305",
          "312",
          "316",
          "317",
          "318",
          "398",
          "399",
          "400",
          "407",
          "402",
          "403",
          "405",
          "408",
          "410",
          "416",
          "417",
          "418",
          "420",
          "421",
          "422",
          "423",
          "425",
          "426",
          "444",
          "430",
          "433",
          "434",
          "435",
          "436",
          "438",
          "440",
          "441",
          "475",
          "478",
          "480",
          "481",
          "483",
          "484",
          "489",
          "491",
          "494",
          "495",
          "498",
          "499",
          "500",
          "503",
          "504",
          "505",
          "508",
          "507",
          "529",
          "531",
          "535",
          "536",
          "538",
          "541",
          "543",
          "545",
          "560",
          "561",
          "562",
          "563",
          "564",
          "309",
          "576",
          "577",
          "578",
          "445",
          "580",
          "581",
          "599",
          "583",
          "854",
          "584",
          "588",
          "592",
          "593",
          "595",
          "598",
          "601",
          "604",
          "607",
          "608",
          "609",
          "611",
          "638",
          "614",
          "615",
          "616",
          "619",
          "620",
          "623",
          "624",
          "625",
          "626",
          "630",
          "631",
          "635",
          "636",
          "678",
          "710",
          "680",
          "681",
          "683",
          "684",
          "686",
          "687",
          "689",
          "691",
          "694",
          "697",
          "698",
          "700",
          "702",
          "704",
          "707",
          "729",
          "732",
          "734",
          "736",
          "790",
          "738",
          "739",
          "740",
          "742",
          "743",
          "746",
          "747",
          "748",
          "791",
          "749",
          "751",
          "753",
          "755",
          "758",
          "759",
          "761",
          "762",
          "765",
          "766",
          "768",
          "771",
          "777",
          "778",
          "781",
          "783",
          "831",
          "832",
          "833",
          "834",
          "837",
          "844",
          "845",
          "846",
          "848",
          "849",
          "850",
          "851",
          "853",
          "857",
          "858",
          "859",
          "886",
          "887",
          "889",
          "890",
          "892",
          "893",
          "895",
          "785",
          "905",
          "908",
          "092",
          "915",
          "918",
          "921",
          "922",
          "924",
          "925",
          "927",
          "931",
          "934",
          "935",
          "936",
          "941",
          "946",
          "976",
          "977",
          "980",
          "981",
          "989",
          "992"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

# Region query body
reg_payload = {
  "query": [
    {
      "code": "Alue 2021",
      "selection": {
        "filter": "item",
        "values": [
          "SSS",
          "MK01",
          "MK02",
          "MK04",
          "MK05",
          "MK06",
          "MK07",
          "MK08",
          "MK09",
          "MK10",
          "MK11",
          "MK12",
          "MK13",
          "MK14",
          "MK15",
          "MK16",
          "MK17",
          "MK18",
          "MK19",
          "MK21"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}
# Sub-region query body
sub_reg_payload = {
  "query": [
    {
      "code": "Alue 2021",
      "selection": {
        "filter": "item",
        "values": [
          "SSS",
          "SK011",
          "SK014",
          "SK015",
          "SK016",
          "SK021",
          "SK022",
          "SK023",
          "SK024",
          "SK025",
          "SK041",
          "SK043",
          "SK044",
          "SK051",
          "SK052",
          "SK053",
          "SK061",
          "SK063",
          "SK064",
          "SK068",
          "SK069",
          "SK071",
          "SK081",
          "SK082",
          "SK091",
          "SK093",
          "SK101",
          "SK103",
          "SK105",
          "SK111",
          "SK112",
          "SK113",
          "SK114",
          "SK115",
          "SK122",
          "SK124",
          "SK125",
          "SK131",
          "SK132",
          "SK133",
          "SK134",
          "SK135",
          "SK138",
          "SK141",
          "SK142",
          "SK144",
          "SK146",
          "SK152",
          "SK153",
          "SK154",
          "SK161",
          "SK162",
          "SK171",
          "SK173",
          "SK174",
          "SK175",
          "SK176",
          "SK177",
          "SK178",
          "SK181",
          "SK182",
          "SK191",
          "SK192",
          "SK193",
          "SK194",
          "SK196",
          "SK197",
          "SK211",
          "SK212",
          "SK213"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}


queries = {'Region':reg_payload,
           'Sub-region':sub_reg_payload,
           'Municipality':mun_payload}

def get_data(region_level):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    
    json = requests.post(url, json = queries[region_level], headers = headers).json()



    cities = list(json['dimension']['Alue 2021']['category']['label'].values())
    
    dimensions = list(json['dimension']['Tiedot']['category']['label'].values())

    values = json['value']

    cities_df = pd.DataFrame(cities, columns = ['Region'])
    cities_df['index'] = 0
    dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
    dimensions_df['index'] = 0

    data = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer').drop('index',axis = 1)
    data['value'] = values
    data = pd.pivot_table(data, values = 'value', index = ['Region'], columns = 'dimensions')
    
    return data

municipal_data = get_data('Municipality')
subregions_data = get_data('Sub-region')
regions_data = get_data('Region')

whole_country_df = municipal_data.loc['WHOLE COUNTRY']

municipal_data.drop('WHOLE COUNTRY', axis=0, inplace = True)
subregions_data.drop('WHOLE COUNTRY', axis=0, inplace = True)
regions_data.drop('WHOLE COUNTRY', axis=0, inplace = True)


# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:kunta1000k_2021&outputFormat=json
with open('assets/municipalities.json', encoding = 'ISO-8859-1') as f:
    municipalities_json = orjson.loads(f.read())
    
# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=maakunta1000k_2021&outputFormat=json
with open('assets/regions.json', encoding = 'ISO-8859-1') as f:
    regions_json = orjson.loads(f.read())

# https://geo.stat.fi/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=tilastointialueet:seutukunta1000k_2021&outputFormat=json    
with open('assets/sub-regions.json', encoding = 'utf-8') as f:
    subregions_json = orjson.loads(f.read())
    
geojson_collection = {'Municipality':municipalities_json, 'Region':regions_json,'Sub-region': subregions_json}
data_collection =  {'Municipality':municipal_data, 'Region':regions_data,'Sub-region': subregions_data}

key_figures = sorted(list(pd.unique(regions_data.columns)))

external_stylesheets = [dbc.themes.SUPERHERO]

app = Dash(name = __name__, external_stylesheets = external_stylesheets, prevent_initial_callbacks=False)
app.title = "Finland's Regional Key Figures"
server = app.server

def serve_layout():
    
    return dbc.Container([
        
        html.Div("Finland's Regional Key Figures",style={'textAlign':'center'}, className="mb-3 mt-3 fw-bold display-1"),

        dbc.Row([
            
            dbc.Col([
                html.H2('Key figure'),
                dcc.Dropdown(id = 'key-figures-finland-key-figure-selection-x',
                             options = [{'label':kf, 'value':kf} for kf in key_figures],
                             value = "Degree of urbanisation, %, 2020",
                             multi = False,
                             style = {'font-size':20, 'font-family':'Arial','color': 'black'}
                             ),
                html.Br(),
                html.H2('Regional level'),
                dcc.Dropdown(id = 'key-figures-finland-region-selection-x',
                             options = [{'label':region, 'value':region} for region in data_collection.keys()],
                             value = 'Region',
                             multi = False,
                             style = {'font-size':20, 'font-family':'Arial','color': 'black'}
                             ),
                html.H1(id = 'key-figures-finland-whole-country-header-x', style = {'textAlign':'center'}, className="mt-5 display-2"),
                html.Div(['Data by ',html.A('Statistics Finland', href = 'https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/kuntien_avainluvut_2021_viimeisin.px/', target = '_blank')], className="text-center fs-3 text"),
                
                ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, align = 'center'),
            dbc.Col([
                html.H1(id = 'key-figures-finland-header-x', style = {'textAlign':'center'}, className="mb-3 mt-3 display-3"),
                dcc.Graph(id = 'key-figures-finland-region-map-x', figure = px.choropleth_mapbox(center = {"lat": 64.961093, "lon": 27.590605})),
                
                dbc.Row([
                
                    dbc.Col([
                        html.H3('Change map type', className = 'mt-2'),
                        dcc.Dropdown(id = 'key-figures-finland-map-type-x', 
                                     options = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" ,"stamen-watercolor"],
                                     value = "open-street-map",
                                     multi = False,
                                     style = {'fontSize':'1.2rem', 'color': 'black','whiteSpace': 'nowrap'})
                        ]),
                    dbc.Col([
                        html.H3('Change colorscale', className = 'mt-2'),
                        dcc.Dropdown(id = 'key-figures-finland-map-colorscale-x', 
                                     options = ['Blackbody','Bluered','Blues','Cividis','Earth','Electric','Greens','Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds','Viridis','YlGnBu','YlOrRd'],
                                     value = "Viridis",
                                     multi = False,
                                     style = {'fontSize':'1.2rem', 'color': 'black','whiteSpace': 'nowrap'})
                        ])
                    ])
                
                ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6)

            ], justify = 'center', className = "m-auto d-flex justify-content-center"),
        dcc.Store(id = 'key-figures-finland-geojson-data', data = geojson_collection['Region']),
        dcc.Store(id = 'key-figures-finland-locations-x'),
        dcc.Store(id = 'key-figures-finland-zs-x'),
        ], fluid = True)    


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
    Output('key-figures-finland-geojson-data','data'),
    Input('key-figures-finland-region-selection-x','value')  
)
def store_geojson(region):        
    return geojson_collection[region]

@app.callback(

    Output('key-figures-finland-locations-x','data'),
    Output('key-figures-finland-zs-x','data'),
    Input('key-figures-finland-key-figure-selection-x','value'),
    Input('key-figures-finland-region-selection-x','value')     
    
)
def store_data(key_figure, region):
    df = data_collection[region][key_figure]
    return list(df.index), list(df.values)

app.clientside_callback(

"""
    function(geojson, locations, z, map_type, colorscale){           
       
        var layout = {
            'height':800,
            'mapbox': {'style':map_type,'zoom':4.2,'center':{'lat': 64.961093, 'lon': 27.590605}
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
Output('key-figures-finland-region-map-x', 'figure'),
Input('key-figures-finland-geojson-data','data'),
Input('key-figures-finland-locations-x','data'),
Input('key-figures-finland-zs-x','data'),
Input('key-figures-finland-map-type-x', 'value'),
Input('key-figures-finland-map-colorscale-x', 'value')     
)

app.layout = serve_layout
if __name__ == "__main__":
    app.run_server(debug=False)   
