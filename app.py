from flask import Flask
from Bot.Consultas import bp_request
import logging
from dotenv import load_dotenv
import yaml

load_dotenv()

logging.basicConfig(
    filename="flask_dt.log",              # archivo log
    level=logging.INFO,              # nivel mínimo a registrar
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app = Flask(__name__)

with open("Bot/Config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f) or {}

app.config["BOT_CFG"] = cfg
app.register_blueprint(bp_request)

if __name__ == '__main__':
    app.run(debug=True)
    