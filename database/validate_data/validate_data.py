from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

# def validate_post_arguments(data, arguments):
#     valid = True
#     for argument in arguments:
#         if not data.get(argument) or argument not in data:
#             valid = False

#     return valid


def validate_data(data, object):
    try:
        validate(data, object)
    except ValidationError as e:
        val_error = ''
        path = e.relative_path
        for p in path:
            val_error += ' > ' + p
        message = val_error + ' ' + e.message
        return {'ok': False, 'message': message}
    except SchemaError as e:
        schema_error = ''
        path = e.relative_path
        for p in path:
            schema_error += ' > ' + p
        message = schema_error + ' ' + e.message
        return {'ok': False, 'message': message}
    return {'ok': True, 'data': data}
