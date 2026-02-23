from flask import Flask
from Bot.Consultas import bp_request

app = Flask(__name__)
app.register_blueprint(bp_request)

if __name__ == '__main__':
    app.run(debug=True)