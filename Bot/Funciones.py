import json
import requests
import os
import random
from time import sleep
from deep_translator import GoogleTranslator
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_msg_server_respond(code:int, msg:str=None, error:bool = False):
    status_msg = None
    meme = ""
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
    if error:        
        meme = get_meme_random(current_app.config["BOT_CFG"])
        
    _dict = {"code": code, "msg": (status_msg if error else msg), "error": error, "meme": meme}
    
    if error:
        logger.error(_dict)
    else:
        logger.info(_dict)
    
    return _dict

def get_geographical_position(comuna:str, pais:str):
    
    _list = []
    
    url = "https://geocoding-api.open-meteo.com/v1/search"
    payload ={
        "name": comuna,
        "count": 10,
        "language": "es",
        "format": "json",
        "countryCode": pais
    }
    
    resp = requests.get(url, params=payload).json()
    _list = [dict(
        latitude=row.get("latitude"),
        longitude = row.get("longitude"),
        comuna= row.get("admin3"),
        provincia= row.get("admin2"),
        region= row.get("admin1"),
        pais= row.get("country"),
        zone = row.get("name")
        ) for row in resp.get("results", [])]

    return _list


def get_weather_api(zones:list):    
    url = "https://api.open-meteo.com/v1/forecast"
    final = ""
    for row in zones:
        payload ={
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "current": "precipitation,is_day,apparent_temperature,wind_speed_10m,relative_humidity_2m"
        }
        _json = requests.get(url, params=payload).json()
        
        if _json.get("current", {}):
            zone = f"{row['zone']}, {row['comuna']}, {row['provincia']}, {row['region']}, {row['pais']}"
            desc = f"{_json['current']['apparent_temperature']} {_json['current_units']['apparent_temperature']}"
            final += f"{zone}: {desc}\n"
            sleep(1)    
    return final

def get_joke_api():
    url = "https://v2.jokeapi.dev/joke/Any"
    res = requests.get(url).json()
    final = ''
    if res.get("setup", {}):
        final = f"{GoogleTranslator(source='auto', target='es').translate(res.get("setup"))}\nResp: {GoogleTranslator(source='auto', target='es').translate(res.get("delivery"))}"
    elif res.get("joke", {}):
        final = f"{GoogleTranslator(source='auto', target='es').translate(res.get("joke"))}"
    
    return final

def get_meme_random(topic:tuple):
    _return  = None
    API_KEY = os.getenv("API_KEY") 
    
    queries = [
        "chavo del 8, chavo",
        "chapulin colorado, chapulin"
    ]

    query = random.choice(queries)

    url = "https://api.giphy.com/v1/gifs/random"
    params = {
        "api_key": API_KEY,
        "tag": query,
        "rating": "g"
    }
    res = requests.get(url, params=params).json()
    data = res.get("data", [])
    if data.get("images", {}).get("downsized", {}).get("url", {}):
        _return = data["images"]["downsized"]["url"]
    
    return _return