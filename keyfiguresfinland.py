# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from dash_iconify import DashIconify
import plotly.express as px
import orjson
import requests




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

def get_data(region_level, lang = 'en'):
    
    # Query url
    url = "https://pxdata.stat.fi:443/PxWeb/api/v1/"+lang+"/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_viimeisin.px"
    
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

# Whole country figures on a pandas Dataframe.
# Extract information from the key figure names.
whole_country_df = pd.DataFrame(regions_data.loc['WHOLE COUNTRY'])
whole_country_df = whole_country_df.rename(columns = {'WHOLE COUNTRY':'value'})
whole_country_df['year'] = [stat.split(', ')[-1] for stat in whole_country_df.index]
whole_country_df['unit'] = [stat.split(', ')[-2] if len(stat.split(', ')) > 2 else '' for stat in whole_country_df.index]
whole_country_df['stat_name'] = [stat.split(', ')[0] if len(stat.split(', ')) < 4 else ', '.join(stat.split(', ')[:2]) for stat in whole_country_df.index]

municipal_data.drop('WHOLE COUNTRY', axis=0, inplace = True)
subregions_data.drop('WHOLE COUNTRY', axis=0, inplace = True)
regions_data.drop('WHOLE COUNTRY', axis=0, inplace = True)




# Municipality timeseries body

mun_series_payload = {
  "query": [
    {
      "code": "Alue 2021",
      "selection": {
        "filter": "item",
        "values": [
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
    },
    {
      "code": "Vuosi",
      "selection": {
        "filter": "item"
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

# Region timeseries body
reg_series_payload = {
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
# Sub-region timeseries body
subreg_series_payload = {
  "query": [
    {
      "code": "Alue 2021",
      "selection": {
        "filter": "item",
        "values": [
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

time_series_queries = {'Region':reg_series_payload,
           'Sub-region':subreg_series_payload,
            'Municipality':mun_series_payload
           }

def get_time_series_data(region_level, lang = 'en', split = 10):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
 'Content-Type': 'application/json'}
    
    
    series_url = "https://pxdata.stat.fi:443/PxWeb/api/v1/"+lang+"/Kuntien_avainluvut/2021/kuntien_avainluvut_2021_aikasarja.px"
    
    if region_level == 'Municipality':
        
        year_lists = np.array_split([str(c) for c in requests.get(series_url).json()['variables'][-1]['values']], split)
        
        dfs = []
        
        for year_list in year_lists:
            mun_series_payload['query'][-1]['selection'] = {'filter': 'item', 'values': list(year_list)}
            
            json = requests.post(series_url, json = mun_series_payload, headers = headers).json()
            cities = list(json['dimension']['Alue 2021']['category']['label'].values())
    
            dimensions = list(json['dimension']['Tiedot']['category']['label'].values())
            years = list(json['dimension']['Vuosi']['category']['label'].values())
            
            values = json['value']

            cities_df = pd.DataFrame(cities, columns = ['Region'])
            cities_df['index'] = 0
            dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
            dimensions_df['index'] = 0
            years_df = pd.DataFrame(years, columns = ['Year'])
            years_df['index'] = 0

            data = pd.merge(left = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer'),
                            right = years_df, how = 'outer', on = 'index').drop('index',axis = 1)

            data['value'] = values
            data.Year = data.Year.astype(int)
            dfs.append(data.set_index('Region'))
        
        return pd.concat(dfs)

        
    else:
    
        json = requests.post(series_url, json = time_series_queries[region_level], headers = headers).json()



        cities = list(json['dimension']['Alue 2021']['category']['label'].values())

        dimensions = list(json['dimension']['Tiedot']['category']['label'].values())
        years = list(json['dimension']['Vuosi']['category']['label'].values())



        values = json['value']

        cities_df = pd.DataFrame(cities, columns = ['Region'])
        cities_df['index'] = 0
        dimensions_df = pd.DataFrame(dimensions, columns = ['dimensions'])
        dimensions_df['index'] = 0
        years_df = pd.DataFrame(years, columns = ['Year'])
        years_df['index'] = 0

        data = pd.merge(left = pd.merge(left = cities_df, right = dimensions_df, on = 'index', how = 'outer'),
                        right = years_df, how = 'outer', on = 'index').drop('index',axis = 1)

        data['value'] = values
        data.Year = data.Year.astype(int)
    
        return data.set_index('Region')

mun_series_data = get_time_series_data('Municipality')
sub_reg_series_data = get_time_series_data('Sub-region')
reg_series_data = get_time_series_data('Region')

mun_series_data.dropna(subset='value',axis=0, inplace=True)
sub_reg_series_data.dropna(subset='value',axis=0, inplace=True)
reg_series_data.dropna(subset='value',axis=0, inplace=True)


whole_country_series_df = reg_series_data.loc['WHOLE COUNTRY']

reg_series_data.drop('WHOLE COUNTRY', axis=0, inplace = True)

timeseries_data = {'Region':reg_series_data,
            'Sub-region':sub_reg_series_data,
            'Municipality':mun_series_data
           }


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
data_collection =  {'Municipality':municipal_data, 'Region':regions_data,'Sub-region': subregions_data}

key_figures = sorted(list(pd.unique(regions_data.columns)))

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

external_stylesheets = [dbc.themes.LUX,
                        dbc.icons.BOOTSTRAP,
                        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                        dbc_css]

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

footer = dbc.Card([
        
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
                                dbc.NavItem(id = 'email',children = [dbc.NavLink(html.I(className="bi bi-envelope"), href="mailto:tuomas.poukkula@gofore.com?subject=Key Figures Finland",external_link=True, target='_blank')] ),
                                
                            ]
                            ),
                             id="navbar-collapse",
                             is_open=False,
                             navbar=True
                           )
                          ]
                    )
                ], className = "d-flex justify-content-end"),
        
        # dbc.Row([
        #     dbc.Col([dbc.DropdownMenu(id ='dd_menu',
        #                               # size="lg",
        #                               # menu_variant="dark",
        #                               children =
        #                                     [
        #                                         dbc.DropdownMenuItem('FI',id = 'fi',  href='/'),
        #                                         dbc.DropdownMenuItem('EN',id = 'en',  href='/en'),
        #                                           dbc.DropdownMenuItem('SV',id = 'sv',  href='/sv')
        #                                     ],
        #         # nav=True,
        #         label="文 / A"
        #     )], align = 'center')
            
        #       ], align = 'center', className = "d-flex justify-content-end"),

    
      ],className='d-flex justify-content-between align-middle', fluid=True
        ),
                            
    color="primary",
    dark=True,
    className = 'navbar navbar-default navbar-static-top mb-5'
    )

app = Dash(name = __name__, external_stylesheets = external_stylesheets, prevent_initial_callbacks=False)
app.title = "Finland's Regional Key Figures"
server = app.server

app.layout = dbc.Container([
    
        navbar,
                
        html.H1("Finland's Key Figures", className = 'fw-bold display-1 text-center'),
        
        
            
            dbc.Row([
                
                
                dbc.Col([
                    
                    dbc.Card([
                        dbc.CardBody([
                    
                            dbc.Row([
                                
                                dbc.Col([
                                
                                    html.H2('Key figure'),
                                    dcc.Dropdown(id = 'key-figures-finland-key-figure-selection-x',
                                                 options = key_figures,
                                                 value = "Degree of urbanisation, %, 2020",
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    ]),
                                dbc.Col([
                                    html.H2('Regional level'),
                                    dcc.Dropdown(id = 'key-figures-finland-region-selection-x',
                                                 options = sorted(list(data_collection.keys())),
                                                 value = 'Region',
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    ])
                                ]),
                            html.Div(id = 'key-figures-finland-whole-country-header-x', className="text-center card-title mt-5 mb-3"),
            
                            dcc.Graph(id = 'key-figures-finland-timeseries-x', className="border"),
                           
                            dbc.Row([
                            
                                dbc.Col([
                                    html.H3('Change chart type', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-chart-selection-x',
                                                 options = ['area', 'line'],
                                                 value = 'line',
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    
                                    ]),
                                dbc.Col([
                                    
                                    html.H3('Change chart template', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-chart-template-x',
                                                 options = sorted([
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
                                                 ]),
                                                 value = "bootstrap_theme",
                                                 className = 'text-dark bg-light text-nowrap'
                                                 )
                                    
                                ]),
                            
                                
                            ]),
                            
                            
                            ]),
                         dbc.CardFooter(['Data by ',html.A('Statistics Finland', href = 'https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/', target = '_blank')], className="text-center align-middle card-text fs-3 text mt-3")
                        
                        ], style = {'height':'100%'}),
                    
                    ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6, align = 'start'),
                dbc.Col([
                    
                    dbc.Card([
                        
                        dbc.CardBody([
                    
                            html.H1(id = 'key-figures-finland-header-x', className="mb-3 mt-3 display-3 card-title text-center"),
                            dcc.Graph(id = 'key-figures-finland-region-map-x', 
                              figure = px.choropleth_mapbox(center = {"lat": 64.961093, "lon": 27.590605}), 
                              clear_on_unhover=True,
                              className = 'border'),
                    
                            dbc.Row([
                    
                                dbc.Col([
                                    html.H3('Change map type', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-map-type-x', 
                                                 options = sorted(["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" ,"stamen-watercolor"]),
                                                 value = "stamen-terrain",
                                                 className = 'text-dark bg-light text-nowrap')
                                    ]),
                                dbc.Col([
                                    html.H3('Change colorscale', className = 'mt-2'),
                                    dcc.Dropdown(id = 'key-figures-finland-map-colorscale-x', 
                                                 options = sorted(['Blackbody','Bluered','Blues','Cividis','Earth','Electric','Greens','Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds','Viridis','YlGnBu','YlOrRd']),
                                                 value = "RdBu",
                                                 className = 'text-dark bg-light text-nowrap')
                                    ]),
                                 # dbc.CardFooter(['Data by ',html.A('Statistics Finland', href = 'https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/', target = '_blank')], className="text-center align-middle card-text fs-3 text mt-3")
                                ])
                            ]),
                         # dbc.CardFooter(['Data by ',html.A('Statistics Finland', href = 'https://pxdata.stat.fi/PxWeb/pxweb/en/Kuntien_avainluvut/Kuntien_avainluvut__2021/', target = '_blank')], className="text-center align-middle card-text fs-3 text mt-3")
                        ], style = {'height':'100%'})
                    
                    ], xs = 12, sm = 12, md = 12, lg = 6, xl = 6, xxl = 6)
    
                ], justify = 'center', className = "mt-3 d-flex justify-content-center"),
            
        
        dcc.Store(id = 'key-figures-finland-geojson-data', data = geojson_collection['Region']),
        dcc.Store(id = 'key-figures-finland-locations-x'),
        dcc.Store(id = 'key-figures-finland-zs-x'),
        footer,
        #dcc.Store(id = 'key-figures-finland-clientside-figure-store-x')

        ], fluid = True,className = 'dbc')    


#app.clientside_callback(
#    """
#   function(figure) {
#       if(figure === undefined) {
#            return {'data': [], 'layout': {}};
#       }
#       const fig = Object.assign({}, figure, {
#          'layout': {
#               ...figure.layout,
#               'yaxis': {
#                    ...figure.layout.yaxis
#                }
#             }
#        });
#        return fig;
#    }
#    """,
#    Output('key-figures-finland-timeseries-x', 'figure'),
#    Input('key-figures-finland-clientside-figure-store-x', 'data')
#)

@app.callback(

    
    #Output('key-figures-finland-clientside-figure-store-x', 'data'),
    Output('key-figures-finland-timeseries-x','figure'),
    Input('key-figures-finland-key-figure-selection-x', 'value'),
    Input('key-figures-finland-region-map-x', 'hoverData'),
    Input('key-figures-finland-region-map-x', 'clickData'),
    Input('key-figures-finland-region-map-x', 'selectedData'),
    Input('key-figures-finland-chart-selection-x','value'),
    Input(ThemeChangerAIO.ids.radio("key-figures-finland-key-theme-selection-x"), "value"),
    Input('key-figures-finland-chart-template-x','value'),
    State('key-figures-finland-region-selection-x','value')
    
    
)
def update_timeseries_chart(key_figure, hov_data,
                            click_data, 
                            sel_data,  chart_type, theme, template, region):
    
    
    kf = ', '.join(key_figure.split(', ')[:-1])

    
    dff = whole_country_series_df[whole_country_series_df.dimensions == kf].dropna().reset_index()
    
    if sel_data is not None:
        
        location = sorted([point['location'] for point in sel_data['points']])
        
    elif click_data is not None:
        
        location = [click_data['points'][0]['location']]
    
    elif hov_data is not None:
        
        location = [hov_data['points'][0]['location']]
     
    else:
        
        location = ['Finland']
        
        
    try:
        dff = timeseries_data[region].loc[location]
        
    except:
        dff = dff
    

    dff = dff[dff.dimensions==kf].reset_index()
    
    loc_string = {True:location[0], False: f'selected {region}s'.replace('ty','ties').replace('Muni','muni').replace('Region','region').replace('Sub-r','sub-r')}[len(location)==1]
    template = template_from_url(theme) if template == "bootstrap_theme" else template    

    name = dff.dimensions.values[0]
    dff = dff.rename(columns = {'value':name, 'Region':region})
    
    if chart_type == 'line':    
        fig = px.line(dff, x = 'Year', y = name, color = region, template = template, hover_data = [region,'Year',name], title = f'{kf} per year in <b>{loc_string}<b>')
        fig.update_traces(line=dict(width=4))
    else:
        fig = px.area(dff, x = 'Year', y = name, color = region, template = template, hover_data = [region,'Year',name], title = f'{kf} per year in <b>{loc_string}<b>')
    fig.update_layout(margin = dict(l=0,r=0),
                      hoverlabel=dict(font_size=23)
    )
    
    
    
    
    return fig
    # print(fig.to_dict()['data'])
    
    # return dcc.Graph(id = 'key-figures-finland-timeseries-x', figure = fig, className="border")

@app.callback(Output('key-figures-finland-header-x','children'),Input('key-figures-finland-key-figure-selection-x', 'value'),Input('key-figures-finland-region-selection-x', 'value') )
def update_header(key_figure, region_level):
    return f"{key_figure} by {region_level}".capitalize()



@app.callback(Output('key-figures-finland-whole-country-header-x','children'),Input('key-figures-finland-key-figure-selection-x', 'value'))
def update_whole_country_header(key_figure):
    # Get all the header components.
    dff = whole_country_df.loc[key_figure]
    stat_name = dff.stat_name
    stat_unit = dff.unit
    stat_year = dff.year
    stat_value = dff.value
    
    # Change values with no decimals (.0) to int.
    stat_value = {True: int(stat_value), False: stat_value}['.0' in str(stat_value)]
    # Use space as thousand separator.
    stat_value = "{:,}".format(stat_value).replace(',',' ')
    
    return dbc.Card(
        [
            dbc.Row([
                dbc.Col([
                    dbc.CardBody([
                        html.Div([stat_name, ", ", stat_year, " in Finland:"], className="card-title text-primary display-3")
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

@app.callback(
    Output('key-figures-finland-geojson-data','data'),
    Input('key-figures-finland-region-selection-x','value')  
)
def store_geojson(region):        
    return geojson_collection[region]


@app.callback(
    Output('key-figures-finland-region-map-x', 'selectedData'),
    Output('key-figures-finland-region-map-x', 'clickData'),
    Input('key-figures-finland-region-selection-x','value'),
    Input('key-figures-finland-key-figure-selection-x', 'value')
)
def reset_map_selections(kf, reg):        
    return None, None

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
            'mapbox': {'style':map_type,'zoom':4.0,'center':{'lat': 64.961093, 'lon': 27.590605}
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

if __name__ == "__main__":
    app.run_server(debug=False)   
