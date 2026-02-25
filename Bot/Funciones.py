import json
import requests

def get_msg_server_respond(code:int, msg:str=None):
    status_msg = None
    match code:
        case 500:
            status_msg = 'Internal Server Error'
        case 502:
            status_msg = 'Bad Gateway'
        case 503:
            status_msg = 'Service Unavailable'
        case 504:
            status_msg = 'Gateway Timeout'
        case 400:
            status_msg = 'Bad Request' #Datos inválidos
        case 401:
            status_msg = 'Unauthorized' #No autenticado
        case 403:
            status_msg = 'Forbidden'#No permitido
        case 404:
            status_msg = 'Not Found' #Endpoint no existe
        case 405:
            status_msg = 'Method Not Allowed'#GET en vez de POST
        case 409:
            status_msg = 'Conflict'#Recurso ya existe
        case 422:
            status_msg = 'Unprocessable Entity'#Validación fallida
        case 301:
            status_msg = 'Moved Permanently'
        case 302:
            status_msg = 'Found'
        case 304:
            status_msg = 'Not Modified'
        case 200: 
            status_msg = 'OK'
        case 201: 
            status_msg = 'Created'
        case 202: 
            status_msg = 'Accepted'
        case 204: 
            status_msg = 'No Content'
        case _:
            status_msg = 'Code Not Found'
            
    _dict = {"respond": status_msg, "code": code, "msg": (msg or "")}
    
    return _dict

def get_geographical_position(comuna:str, pais:str):
    
    latitude = None
    longitude = None
    
    url = "https://geocoding-api.open-meteo.com/v1/search"
    payload ={
        "name": comuna,
        "count": 1,
        "language": "es",
        "format": "json",
        "countryCode": pais
    }
    
    resp = requests.get(url, params=payload).json()
    if len(resp.get("results", [])) > 0:
        latitude = resp["results"][0].get("latitude")
        longitude = resp["results"][0].get("longitude")

    return latitude, longitude


def get_weather_api(lat, lon):    
    url = "https://api.open-meteo.com/v1/forecast"
    payload ={
        "latitude": lat,
        "longitude": lon,
        "current": "precipitation,is_day,apparent_temperature,wind_speed_10m,relative_humidity_2m"
    }
    resp = requests.get(url, params=payload).json()
    return resp

def get_joke_api():
    url = "https://v2.jokeapi.dev/joke/Any"
    payload ={
        "lang": "es",
        "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit"
    }
    res = requests.get(url, params = payload).json()
    return res