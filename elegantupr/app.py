from flask import Flask
from flask_cors import CORS

from .parser import parser
from .filter import filter

def create_app():
    """Create Flask app"""
    app = Flask(__name__)

    # register endpoints
    app.register_blueprint(parser)
    app.register_blueprint(filter)

    return app

app = create_app()

# enable CORS
CORS(app)
