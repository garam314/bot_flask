from flask import Blueprint, render_template, request
import yaml
import json
import logging
import traceback
import pycountry
import re
from .Funciones import get_msg_server_respond, get_geographical_position, get_weather_api, get_joke_api

logger = logging.getLogger(__name__)

bp_request = Blueprint("request", __name__, url_prefix="/requests")


def get_help():    
    resp = None
    
    try:
        with open(r"Bot\help.yaml", "r", encoding="utf-8") as file:
            resp = yaml.safe_load(file)
    except Exception as e:
        logger.error(traceback.format_exc())
        resp = get_msg_server_respond(400)
        
    return resp

def get_weather(location):
    resp = None
    try:
        pattern = r"^\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*,\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*$"
        match = re.match(pattern, location)
        if match:
            ciudad, pais = match.groups()
        else:
            resp = get_msg_server_respond(400, "MAL FORMADO")
            return resp
        
        code_country = pycountry.countries.get(name=pais)
        lat, lon = get_geographical_position(ciudad, code_country.alpha_2)
        _json = get_weather_api(lat, lon)

        if _json.get('error', False):
            resp = get_msg_server_respond(400, resp["reason"])
        else:
            resp = get_msg_server_respond(200)
            resp['data'] = dict(
                temp = f"{_json['current']['apparent_temperature']} {_json['current_units']['apparent_temperature']}",
                humidity = f"{_json['current']['relative_humidity_2m']} {_json['current_units']['relative_humidity_2m']}",
                )
        
        return resp            
        
    except Exception:
        logger.error(traceback.format_exc())
        resp = get_msg_server_respond(400)
        return resp
    
def get_joke():
    _json = get_joke_api()
    resp = None
    
    if _json.get("error", False):
        resp = get_msg_server_respond(400)
        logger.error(resp['additionalInfo'])
    else:
        resp = get_msg_server_respond(200)
        resp['data'] = {}
        resp['data'] = dict(
            joke = _json.get("joke") if _json.get("type") == "single" else _json.get("setup"),
            resp = _json.get("delivery", "")
        )
    return resp
        

@bp_request.route("/", methods=["POST"])
def managment_request():
    msg = request.form.get("command", default=None)
    resp = None
    if not msg:
        resp = get_msg_server_respond(400)
        
    if msg.startswith('!'):
        command = msg.split(" ")[0].lower()
        match command:
            case "!help":
                resp = get_help()
            case "!clima":
                try:
                    resp = get_weather(" ".join(msg.split(" ")[1:]))                    
                except IndexError:
                    resp = get_msg_server_respond(400, "y yo adivino que clima quieres ver")
            case "!chiste":
                resp = get_joke()
    return json.dumps(resp)