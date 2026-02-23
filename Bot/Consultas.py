from flask import Blueprint, render_template
import json

bp_request = Blueprint("request", __name__, url_prefix="/requests")


@bp_request.route("/", methods=["POST"])
def get_data(message: str):
    message = (message or "").strip()
    if not message:
        return json.dumps({"code": 400, "msg": "Opcion no valida"})