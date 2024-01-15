weather_codes = {
    0 : ['clear sky','Despejado','☀️'],
    1 : ['mainly clear','Mayorm. Despej.','🌤️'],
    2 : ['partly cloudy','Parcialm. Nublado','⛅'],
    3 : ['overcast','Nublado','☁️'],
    45: ['fog','Niebla','🌫️'],
    48: ['depositing rime fog','?depositing rime fog','❓'],
    51: ['light drizzle','Llovizna Ligera','🌧️'],
    53: ['moderate drizzle','Llovizna Moderada','🌧️'],
    55: ['dense drizzle','Llovizna Densa','🌧️'],
    56: ['light freezing drizzle','Llovizna Ligera Congelada','🌧️'],
    57: ['moderate or dense freezing drizzle','Llovizna Congelada Moderada o Densa','🌧️'],
    61: ['light rain','Lluvia Ligera','🌧️'],
    63: ['moderate rain','Lluvia Moderada','🌧️'],
    65: ['heavy rain','Fuertes Lluvias','🌧️'],
    66: ['light freezing rain','Lluvia Ligera Congelada','🌧️'],
    67: ['moderate or heavy freezing rain','Lluvia Congelada Moderada o Fuerte','🌧️'],
    71: ['slight snowfall','Nieve Ligera','🌨️'],
    73: ['moderate snowfall','Nieve Moderada','🌨️'],
    75: ['heavy snowfall','Fuertes Nevadas','🌨️'],
    77: ['snow grains','?snow grains','🌨️'],
    80: ['slight rain showers','Lluvia Intermit. Ligera','🌦️'],
    81: ['moderate rain showers','Lluvia Intermit. Moderada','🌦️'],
    82: ['heavy rain showers','Fuertes Lluvias Intermit.','🌦️'],
    85: ['slight snow showers','Nieve Intermitente Ligera','🌨️'],
    86: ['heavy snow showers','Fuertes Nevadas Intermitentes','🌨️'],
    95: ['thunderstorm slight or moderate','Tormenta','🌩️'],
    96: ['thunderstorm strong','Tormenta Fuerte','🌩️'],
    99: ['thunderstorm heavy','Tormenta Fuerte','🌩️']
}

dict_reg_names = {
    'Norte':'NOR',
    'Centro':'CEN',
    'Sur':'SUR'
}

dict_locations = {
    'Concordia': [-31.393,-58.0209, 0] , #lat, lon, indice donde va a aparecer
    'Buenos Aires': [-34.6131 , -58.3772, 1],
    'Gualeguaychú': [-33.0094 , -58.5172, 2]
}

list_locations = list(dict_locations.keys())