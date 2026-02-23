from flask import Blueprint, render_template

bp_request = Blueprint("request", __name__, url_prefix="/requests")


@bp_request.route("/", methods=["POST"])
def get_test():
    return "Hola Mundo"