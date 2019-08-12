from . import api
from flask_restful import Resource

from app.models import *

@api.resource("/hello/")
class Hello(Resource):
    def get(self):
        return {"hello": "world"}