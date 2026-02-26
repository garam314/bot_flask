from flask import Blueprint, render_template, request, jsonify, current_app
import json
import logging
import traceback
import pycountry
import re
import os
from .Funciones import get_msg_server_respond, get_geographical_position, get_weather_api, get_joke_api, get_indicators

logger = logging.getLogger(__name__)
bp_request = Blueprint("request", __name__, url_prefix="/requests")

def get_help():    
    resp = None
    try:
        with open("Bot/Config.yaml", "r", encoding="utf-8") as file:
            _dict = yaml.safe_load(file)
            resp = _dict.get("help", get_msg_server_respond(500, topic=current_app.config["BOT_CFG"]))
    except Exception as e:
        logger.error(traceback.format_exc())
        resp = get_msg_server_respond(400, topic=current_app.config["BOT_CFG"])
    return resp

def get_weather(location):
    resp = None
    try:
        pattern = r"^\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*,\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*$"
        match = re.match(pattern, location)
        if match:
            ciudad, pais = match.groups()
        else:
            resp = get_msg_server_respond(400, msg="MAL FORMADO", topic=current_app.config["BOT_CFG"])
            return resp

        code_country = pycountry.countries.get(name=pais)
        zones = get_geographical_position(ciudad, code_country.alpha_2)
        list_weather = get_weather_api(zones)

        if not list_weather:
            resp = get_msg_server_respond(400, topic = current_app.config["BOT_CFG"])
        else:
            resp = get_msg_server_respond(200)
            resp['data'] = list_weather
                    
        return resp            
        
    except Exception:
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        resp = get_msg_server_respond(400, topic=current_app.config["BOT_CFG"])
        return resp
    
def get_joke():
    _json = get_joke_api()
    resp = None
    
    if _json.get("error", False):
        resp = get_msg_server_respond(400, topic=current_app.config["BOT_CFG"])
        logger.error(resp['additionalInfo'])
        print(traceback.format_exc())
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
    msg = request.args.get("command", default=None)
    resp = None
    if not msg:
        resp = get_msg_server_respond(400, topic=current_app.config["BOT_CFG"])
    else:
        if msg.startswith('!'):
            command = msg.split(" ")[0].lower()
            match command:
                case "!help":
                    resp = get_help()
                case "!clima":
                    lugar = msg.split(" ")[1:]
                    if not lugar:
                        resp = get_msg_server_respond(400, msg = "y yo adivino que clima quieres ver", topic=current_app.config["BOT_CFG"])
                    else:
                        resp = get_weather(" ".join(lugar))
                        
                case "!chiste":
                    resp = get_joke()
                case _:
                    resp = get_msg_server_respond(404, topic=current_app.config["BOT_CFG"])
    return jsonify(resp)