
from flask import Blueprint
from flask_restx import Api
from app.api.v1.places import api as places_ns

# Création du blueprint
bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Création de l'API RESTx
api = Api(bp, doc='/docs')

# Enregistrement du namespace avec le chemin correct
api.add_namespace(places_ns, path='/places')
