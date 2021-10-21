from flask import jsonify


def json_response(message, code, data={}):
    Invaild_request = 'Invalid request'
    ok = False
    if code == 200:
        ok = True

    response = jsonify({'success': ok, 'message': message, 'data': data}), code
    return response


def bad_request(error=''):
    message = 'Bad request parameters!' + error
    return json_response(message, 400)
