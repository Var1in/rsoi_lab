import json
from playhouse.shortcuts import model_to_dict
from os import getenv as env

from flask import make_response, request

from src.static.entities.person import Person

from src.static import routes
from . import reserve_service_path
from ..entities.hotels import Hotels

flask_blueprint = routes


@flask_blueprint.route(reserve_service_path + '/hotels', methods=['GET'])
def get_all_hotels():
    params = request.args
    page = int(params.get('page', 1))
    size = int(params.get('size', 1))

    hotels = Hotels.select().dicts()

    result = [
        value for value in hotels
    ]

    result = result[((page - 1) * size):(page * size)]

    response = {
        "page": page,
        "pageSize": size,
        "totalElements": len(result),
        "items": result
    }

    return make_response(
        response,
        200)