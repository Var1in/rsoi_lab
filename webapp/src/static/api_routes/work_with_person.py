import json

from flask import make_response, request

from src.static.entities.person import Person

from src.static import routes
from . import base_path

flask_blueprint = routes

mapping = base_path + '/persons'


@flask_blueprint.route(mapping, methods=['GET'])
def give_all_persons():
    persons = Person.select().dicts()
    return [
        value for value in persons
    ]


@flask_blueprint.route(mapping + '/<person_id>', methods=['GET'])
def give_single_person(person_id=None):
    if person_id is None:
        return make_response(
            {'message': 'No value entered'},
            400
        )

    persons = Person.select().where(Person.id == person_id).dicts()
    response = None

    for person in persons:
        response = person

    if response is None:
        return make_response({
            'message': 'No person found'},
            400
        )

    return response


@flask_blueprint.route(mapping, methods=['POST'])
def create_new_person():
    required_fields = {
        'name': str,
        'age': int,
        'address': str,
        'work': str
    }
    if len(request.data) == 0 and len(request.form) == 0:
        return make_response({
            'message': 'Invalid data',
            'errors': {
                field: 'string' if f_type is str else 'integer' for field, f_type in required_fields.items()
            },
            'entered_data': request.data.decode()
        }, 400)

    if len(request.data) == 0:
        request_json = request.form.to_dict()
    else:
        request_json = json.loads(request.data)

    errors = {}
    for field, f_type in required_fields.items():

        if (value := request_json.get(field)) is None:
            errors[field] = 'string' if f_type is str else 'integer'
            continue

        try:
            request_json[field] = f_type(value)
        except ValueError:
            errors[field] = 'string' if f_type is str else 'integer'

    if len(errors.keys()) > 0:
        return make_response({
            'message': 'Invalid data',
            'errors': {
                field: 'string' if f_type is str else 'integer' for field, f_type in errors.items()
            }
        }, 400)

    person = Person.create(**request_json)
    Person.save(person)
    return make_response(
        {},
        201
    )


@flask_blueprint.route(mapping + '/<person_id>', methods=['DELETE'])
def delete_person_by_id(person_id=None):

    if person_id is None:
        return make_response(
            {'message': 'No value entered'},
            400
        )
    if not str(person_id).isnumeric():
        return make_response(
            {'message': 'Incorrect value'},
            400
        )

    person_id = int(person_id)
    try:
        person = Person.get(Person.id == person_id)
    except Exception:
        return make_response(
            {'message': 'Person not found'},
            400
        )
    person.delete_instance()

    return make_response(
        {},
        204
    )



@flask_blueprint.route(mapping + '/<person_id>', methods=['PATCH'])
def modify_person_by_id(person_id=None):
    if person_id is None:
        return make_response(
            {'message': 'No value (person_id) entered'},
            400
        )
    if not str(person_id).isnumeric():
        return make_response(
            {'message': 'Incorrect value person_id'},
            400
        )
    required_fields = {
        'name': str,
        'age': int,
        'address': str,
        'work': str
    }
    if len(request.data) == 0 and len(request.form) == 0:
        return make_response({
            'message': 'Invalid data',
            'errors': {
                field: 'string' if f_type is str else 'integer' for field, f_type in required_fields.items()
            }
        }, 400)

    if len(request.data) == 0:
        request_json = request.form.to_dict()
    else:
        request_json = json.loads(request.data)

    errors = {}
    for field, f_type in required_fields.items():

        if (value := request_json.get(field)) is None:
            errors[field] = 'string' if f_type is str else 'integer'
            continue

        try:
            request_json[field] = f_type(value)
        except ValueError:
            errors[field] = 'string' if f_type is str else 'integer'

    if len(errors.keys()) > 0:
        return make_response({
            'message': 'Invalid data',
            'errors': {
                field: 'string' if f_type is str else 'integer' for field, f_type in errors.items()
            }
        }, 400)

    person_id = int(person_id)
    try:
        person = Person.get(Person.id == person_id)
    except Exception:
        return make_response(
            {'message': 'Person not found'},
            400
        )

    for field in required_fields:
        setattr(person, field, request_json[field])
    person.save()
    return make_response(
        {"message": 'Person for ID was updated'},
        200
    )
