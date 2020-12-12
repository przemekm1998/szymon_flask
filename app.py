from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

from api.routes import initialize_routes

initialize_routes(api)
