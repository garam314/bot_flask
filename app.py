from flask import Flask
from Bot.Consultas import bp_request
import logging

logging.basicConfig(
    filename="flask_dt.log",              # archivo log
    level=logging.INFO,              # nivel mínimo a registrar
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
app.register_blueprint(bp_request)

if __name__ == '__main__':
    app.run(debug=True)