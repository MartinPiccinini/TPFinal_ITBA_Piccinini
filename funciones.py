import requests
from datetime import datetime
from datetime import timedelta
import math
import pandas as pd
import streamlit as st
import re

def find_second():
    
    try_list = [18,19,20,21,22]

    utc_now = datetime.utcnow() - timedelta(minutes=50)

    id_today = datetime.utcnow().strftime('%Y%m%d')

    mins = utc_now.minute

    rounded_mins = math.floor(mins/10)*10

    id_hora = utc_now.hour * 100 + rounded_mins

    correct_seconds = 20

    for i in try_list:
        
        url = f'https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_NOR_ALTA_{id_today}_{id_hora}{i}Z.jpg'

        req = requests.get(url).status_code

        if req == 200:
            correct_seconds = i
            break
        else:
            continue

    return correct_seconds



def list_time_ids(qty_images_wanted: int):

    list_substr = [i*10 for i in range(3,3 + qty_images_wanted)]

    list_ids = []

    id_seconds = find_second()

    for i in list_substr:

        utc_now = datetime.utcnow() - timedelta(minutes=i)

        mins = utc_now.minute

        rounded_mins = math.floor(mins/10)*10

        id_hora = utc_now.hour * 10000 + rounded_mins * 100 + id_seconds

        list_ids.append(str(id_hora))

    list_ids.reverse()

    return list_ids

def get_urls(amt_images_wanted: int, region: str = 'AR'):

    '''
    Region solo puede estar entre ['ARG','NOR','CEN','SUR']
    '''
    
    id_today = datetime.utcnow().strftime('%Y%m%d')

    list_time = list_time_ids(amt_images_wanted)

    list_urls = []

    for i in list_time:

        url_jpg = f'https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_{region}_ALTA_{id_today}_{i}Z.jpg'

        req = requests.get(url_jpg).status_code

        if req == 200:
            list_urls.append(url_jpg)
    
    return list_urls

def get_urls_all_regions(amt_images_wanted: int):

    '''
    Region solo puede estar entre ['ARG','NOR','CEN','SUR']
    '''
    
    id_today = datetime.utcnow().strftime('%Y%m%d')

    list_time = list_time_ids(amt_images_wanted)

    list_reg = ['NOR','CEN']

    dict_reg = {}

    for j in list_reg:  
        list_urls = []
        
        for i in list_time:
            url_jpg = f'https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_{j}_ALTA_{id_today}_{i}Z.jpg'

            req = requests.get(url_jpg).status_code

            if req == 200:
                list_urls.append(url_jpg)
        
        dict_reg[j] = list_urls
            
    return dict_reg

def get_urls_all_regions_noreq(amt_images_wanted: int):

    '''
    Region solo puede estar entre ['ARG','NOR','CEN','SUR']
    '''
    
    id_today = datetime.utcnow().strftime('%Y%m%d')

    list_time = list_time_ids(amt_images_wanted)

    list_reg = ['NOR','CEN','SUR']

    dict_reg = {}

    for j in list_reg:  
        list_urls = []
        
        for i in list_time:
            url_jpg = f'https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_{j}_ALTA_{id_today}_{i}Z.jpg'

            list_urls.append(url_jpg)
        
        dict_reg[j] = list_urls
            
    return dict_reg

def get_weather(lat_lon_list:list = [-31.393, -58.0209]):
	
	url = 'https://api.open-meteo.com/v1/forecast'

	params = {
	"latitude": lat_lon_list[0],
	"longitude": lat_lon_list[1],
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "weather_code", "surface_pressure"],
	"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "precipitation", "weather_code"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "precipitation_sum", "precipitation_probability_max"],
	"timezone": "America/Sao_Paulo"
	}

	req = requests.get(url=url,params=params)

	return req.json()

def convert_date(date_str:str):
    to_dt = datetime.strptime(date_str, '%Y-%m-%d')

    return to_dt.strftime('%d/%m') #to_dt.strftime('%d/%m/%y') con año incluido

def day_weather_label(dict_daily_w:dict,weather_codes_var: dict):
    
    days_req = len(dict_daily_w['time'])

    dict_days = {'d+0': None,
                 'd+1': None,
                 'd+2': None,
                 'd+3': None,
                 'd+4': None,
                 'd+5': None,
                 'd+6': None,
                }

    for i in range(days_req):
        dict_label = f'd+{i}'

        date_iter = convert_date(dict_daily_w['time'][i])

        w_code = dict_daily_w['weather_code'][i]

        prec_prob = dict_daily_w['precipitation_probability_max'][i]

        prec_sum = dict_daily_w['precipitation_sum'][i]

        min_temp = dict_daily_w['temperature_2m_min'][i]

        max_temp = dict_daily_w['temperature_2m_max'][i]
        
        str_weather = f'{date_iter}: {weather_codes_var[w_code][1]} {weather_codes_var[w_code][2]} | Min: {min_temp}°C Max: {max_temp}°C | 💧{prec_prob}% - {prec_sum} mm'

        dict_days[dict_label] = str_weather

    return dict_days

def hourly_weather_dict(weather_dict: dict):

    dict_hourly = weather_dict['hourly']

    df = pd.DataFrame.from_dict(data = dict_hourly,orient='columns')

    df[['date', 'times']] = df.time.str.split("T", expand = True)

    df.drop(['time'],axis=1,inplace=True)

    unique_dates = df.date.unique()
    dict_df = {}
    count_i = 0
    
    for i in unique_dates:
        key_d = f'd+{count_i}'
        df_to_save = df[df.date == i].reset_index(drop=True).drop(['date'],axis=1)
        dict_df[key_d] = df_to_save
        count_i += 1
    
    return dict_df

def print_hourly_weather(df_hrly, weather_codes_var: dict):
        df = df_hrly
        

        
        for i in range(24):
            
            if df.precipitation_probability[i] != 0: 
                var_precip = '- '+  str(df.precipitation[i]) + ' mm' 
            else:
                var_precip = ''
        
        
            st.write(
                f'''{df.times[i]} \n
                {weather_codes_var[df.weather_code[i]][2]} {weather_codes_var[df.weather_code[i]][1]}
    🌡️  {df.temperature_2m[i]}°C ({df.apparent_temperature[i]} ST)
    💧  {df.precipitation_probability[i]}% {var_precip}'''
                )
            
def create_lat_lon_lists(dict_locs:list):
    list_lat = []
    list_lon = []
    for i in dict_locs:
        list_lat.append(dict_locs[i][0])
        list_lon.append(dict_locs[i][1])

    return [list_lat, list_lon]



def get_rates():

    url = 'https://dolarapi.com/v1/dolares'
    
    req = requests.get(url =  url)

    list_rates = req.json()

    dict_rates = {}

    for i in list_rates:
        dict_rates[i['casa']] = {'nombre': i['nombre'],
                                'compra': i['compra'],
                                'venta': i['venta']
                                }
    
    return dict_rates


def rate_card(rate_dict:dict, rate_name:str):
    
    st.write(f'### {rate_dict[rate_name]["nombre"]}')
    st.metric(label = 'Venta', value= format(rate_dict[rate_name]['venta'] , '.2f') )
    st.metric(label = 'Compra', value= format(rate_dict[rate_name]['compra'], '.2f'))

def get_goes_imgs():
    url = 'https://weather.ndc.nasa.gov/cgi-bin/get-abi'

    params = {
        "satellite": 'GOESEastfullDiskband13',
        "lat": -31,
        "lon": -60,
        "zoom": 1,
        "width": 600,
        "height": 600,
        "quality": 55 ,
        "palette": 'ir2.pal' ,
        "type":'Animation'
    }

    r = requests.get(url=url,params=params)

    images_string = list(r.iter_lines())[27]

    jpg_list = re.findall(r'/goes/abi/dynamic/(\w+\.jpg)', images_string.decode('utf-8'))

    image_url = 'https://weather.ndc.nasa.gov/goes/abi/dynamic/'

    url_list = [image_url + i for i in jpg_list]

    return url_list



