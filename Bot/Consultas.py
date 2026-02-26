from flask import Blueprint, render_template, request, jsonify, current_app
import json
import logging
import traceback
import pycountry
import re
import os
from .Funciones import get_msg_server_respond, get_geographical_position, get_weather_api, get_joke_api

logger = logging.getLogger(__name__)
bp_request = Blueprint("request", __name__, url_prefix="/requests")

def get_help():    
    resp = None
    final = ""
    for item, desc in current_app.config["BOT_CFG"].get('help', {}).items():
        final += f"{item}: {desc}.\n"
    
    if final:
        resp = get_msg_server_respond(200, final, False)
    else:
        resp = get_msg_server_respond(404, "Parametros no encontrados", False)
        
    return resp
        

def get_weather(location):
    resp = None
    try:
        pattern = r"^\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*,\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*$"
        match = re.match(pattern, location)
        if match:
            ciudad, pais = match.groups()
        else:
            resp = get_msg_server_respond(400, error=True)
            return resp

        code_country = pycountry.countries.get(name=pais)
        zones = get_geographical_position(ciudad, code_country.alpha_2)
        weather = get_weather_api(zones)

        if weather:
            resp = get_msg_server_respond(200, weather, error=False)
        else:
            resp = get_msg_server_respond(400, error=True)
                    
        return resp            
        
    except Exception:
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        resp = get_msg_server_respond(400, error=True)
        return resp
    
def get_joke():
    joke = get_joke_api()
    resp = None
    
    if joke:
        resp = get_msg_server_respond(200, msg=joke, error=False)
    else:
        resp = get_msg_server_respond(400, error = True)

    return resp
        

@bp_request.route("/", methods=["POST"])
def managment_request():
    try:
        msg = request.args.get("command", default=None)
        resp = None
        if not msg:
            resp = get_msg_server_respond(400, error=True)
        else:
            if msg.startswith('!'):
                command = msg.split(" ")[0].lower()
                match command:
                    case "!help":
                        resp = get_help()
                    case "!clima":
                        lugar = msg.split(" ")[1:]
                        if not lugar:
                            resp = get_msg_server_respond(400, msg = "y yo adivino que clima quieres ver", error=True)
                        else:
                            resp = get_weather(" ".join(lugar))
                    case "!chiste":
                        resp = get_joke()
                    case _:
                        resp = get_msg_server_respond(404, error=True)
    except Exception:
        print(traceback.format_exc())
        resp = get_msg_server_respond(500, msg=traceback.format_exc(), error=True)
    return f"{resp.get("meme", "")}\n{resp["msg"]}"