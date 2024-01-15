import streamlit as st 
import funciones as f_module
import variables as var_mod
import time


st.set_page_config(layout="wide")


#region def cache fns - define las funciones que van a guardar datos en cache
@st.cache_data(show_spinner=False,ttl=3600) # Use Streamlit's caching decorator
def get_cached_urls(amt: int):
    return f_module.get_urls_all_regions(amt)

@st.cache_data(show_spinner=False,ttl=3600) # Use Streamlit's caching decorator
def get_goes_imgs():
    return f_module.get_goes_imgs()

@st.cache_data(show_spinner=False,ttl=3600)
def get_cached_weather(lat_lon_list:list = [-31.393, -58.0209]):
    return f_module.get_weather(lat_lon_list)

@st.cache_data(show_spinner=False,ttl=3600)
def get_cached_rates():
    return f_module.get_rates()
#endregion

#region variables
amt_hrs = 12

location_dict = var_mod.dict_locations

list_latlons = f_module.create_lat_lon_lists(location_dict)

#dict_urls = get_cached_urls(amt_days) # esto se deja comentado porque lo que hace es tirar una request para cada imagen, lo que lo hace lento



#st.components.v1(html = html_str)


dict_urls = get_goes_imgs()


dict_weather_all = get_cached_weather(list_latlons)

dict_rates = get_cached_rates()
#endregion

#region botones
if st.sidebar.button('Actualizar Satélite'):
    get_goes_imgs().clear() 
    st.rerun()

if st.sidebar.button('Actualizar Clima'):
    get_cached_weather.clear()
    st.rerun()

if st.sidebar.button('Actualizar Cotizaciones'):
    get_cached_rates.clear()
    st.rerun()
#endregion

# COMIENZA INFORMACION
st.title('Imágenes satelitales y clima')

#region clima
col1, col2 = st.columns(2)

#region satelite

with col1:

    st.markdown('## Satélite')
    
    col1_1, col1_2, col1_3 = st.columns([4.5,2,1])
    
    with col1_1:
        reg_select = st.selectbox(
        label= 'Región',
        options= ('Norte','Centro','Sur'),
        index= 0 
        )

    num_images = len(dict_urls) - 1 #len(dict_urls[ var_mod.dict_reg_names[reg_select]]) - 1

    with col1_2:
        number = st.number_input(label='Cambiar Horario',
                                min_value=0,
                                max_value = num_images,
                                value = num_images,
                                step=1,
                                key='input_izq'
                                )

    with col1_3:
        '\n'
        '\n'
        if st.button('▶',type = 'primary'):
            animar = True
        else:
            animar = False

    if not animar:
        try:
            st.image(dict_urls[number]) # st.image(dict_urls[ var_mod.dict_reg_names [reg_select]] [number]) #accede a dicc de urls, con la key de la region segun lo que salga en el diccionario de traduccion de regiones en el modulo de variables
        except:
            st.write('No existe imagen para este horario')


    else:
        placeholder = st.empty()

        for img_array in dict_urls: #for img_array in dict_urls[ var_mod.dict_reg_names [reg_select]]:
            placeholder.image(img_array)
            time.sleep(0.5)
        animar = False
        st.rerun()

#endregion

#region forecast
with col2:

    st.markdown('## Clima')

    locat_select = st.selectbox('Localidad:',options=var_mod.list_locations)

    dict_weather = dict_weather_all[location_dict[locat_select][2]]

    dict_wth_current = dict_weather['current']
    f'''#### Actual\n
    {var_mod.weather_codes[dict_wth_current['weather_code']][2]} {var_mod.weather_codes[dict_wth_current['weather_code']][1]}
    🌡️ {dict_wth_current['temperature_2m']}°C ({dict_wth_current['apparent_temperature']} ST) | Humedad {dict_wth_current['relative_humidity_2m']}% | Presión {dict_wth_current['surface_pressure']} hPa
    '''

    st.markdown('#### Semanal')
    dict_wth_daily = f_module.day_weather_label(dict_weather['daily'], var_mod.weather_codes)
    dict_wth_hrly = f_module.hourly_weather_dict(dict_weather)

    with st.expander(label = dict_wth_daily['d+0']):
        
        tab1, tab2 = st.tabs(["Gráfico", "Por Hora"])
        with tab1:
            st.write('Acá iría el gráfico')
        with tab2:
            f_module.print_hourly_weather(dict_wth_hrly['d+0'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+1']):
        f_module.print_hourly_weather(dict_wth_hrly['d+1'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+2']):
        f_module.print_hourly_weather(dict_wth_hrly['d+2'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+3']):
        f_module.print_hourly_weather(dict_wth_hrly['d+3'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+4']):
        f_module.print_hourly_weather(dict_wth_hrly['d+4'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+5']):
        f_module.print_hourly_weather(dict_wth_hrly['d+5'], var_mod.weather_codes)

    with st.expander(label = dict_wth_daily['d+6']):
        f_module.print_hourly_weather(dict_wth_hrly['d+6'], var_mod.weather_codes)
#endregion


#endregion

#region dolar
st.markdown("""---""")
st.markdown('# Cotización Dólares')

col_d1, col_d2 = st.columns(2)

with col_d1:

    f_module.rate_card(rate_dict=dict_rates,rate_name='oficial')

    st.markdown("""---""")

    f_module.rate_card(rate_dict=dict_rates,rate_name='blue')

    st.markdown("""---""")

    f_module.rate_card(rate_dict=dict_rates,rate_name='tarjeta')

    st.markdown("""---""")

with col_d2:

    f_module.rate_card(rate_dict=dict_rates,rate_name='bolsa')

    st.markdown("""---""")

    f_module.rate_card(rate_dict=dict_rates,rate_name='contadoconliqui')

    st.markdown("""---""")

    f_module.rate_card(rate_dict=dict_rates,rate_name='mayorista')

    st.markdown("""---""")
#endregion