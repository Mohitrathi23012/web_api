import os
import argparse
from flask import Flask, request, jsonify ,render_template
import pymongo
from pymongo import MongoClient
import math
import random
from current_time import current_time
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies)
from flask_cors import CORS, cross_origin
from json_encoder import JSONEncoder
import uuid
import json
from random import randint
from flask_bcrypt import Bcrypt
from response import json_response, bad_request

from bson import ObjectId
import string
from database.employee_schema import employee_profile_schema
from database.employee_coll import (
    add_new_vendor, get_all_vendors, update_vendor_data, get_vendor)
from database.employee_docs_coll import add_new_vendor_doc


from database.user_coll import (get_all_users, get_user_data, update_user_data,
                                delete_user, add_action_user_vendor, add_action_user_project,
                                delete_user, add_action_user_vendor, add_action_user_project,
                                delete_user, add_action_user_vendor, add_action_user_project,
                                add_action_user_admin, add_action_user_self)
from database.user_profile_schema import user_profile_schema


from database.validate_data.validate_data import validate_data
from database.validate_data.validate_user_data import (
    otp_check_schema, user_login_check_schema, user_register_check_schema, user_check_schema, update_role_check_schema, user_check_schema_admin_update, delete_user_check_schema, user_change_password_check_schema, reset_password_check_schema)
from database.validate_data.validate_employee_data import(
    employee_profile_check_schema)

from database.project_profile_schema import(
    project_profile_schema, add_project_profile_schema)
from database.projects_coll import add_new_project, get_all_projects, update_project_data, get_project, add_new_project_doc, update_project_cr_data
from database.validate_data.validate_project_data import project_profile_check_schema, add_project_check_schema, add_cr_check_schema, update_cr_check_schema
from werkzeug.utils import secure_filename

import requests

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    app.config.from_pyfile('config.py')
else:

    app.config.from_pyfile('config_dev.py')

jwt = JWTManager(app)
app.json_encoder = JSONEncoder
flask_bcrypt = Bcrypt(app)

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
# parser.add_argument('dbusername', type=str, help='Mongodb username')
# parser.add_argument('mongopassword', type=str, help='Mongodb password')
# parser.add_argument('mongodatabase', type=str, help=' Mongodb ')
# parser.add_argument('appsecret', type=str, help='App secret')   

# args = parser.parse_args()


# dbusername = args.dbusername
# dbpass = args.mongopassword
database = 'projectDB'
cluster = MongoClient('localhost',27017)
# print('mongodb+srv://' + dbusername + ':' + dbpass + '@cluster0.ohisq.mongodb.net/'+database+'?retryWrites=true&w=majority')
db = cluster[database]
collection_user = db['user']
collection_vendors = db['team']
collection_projects = db['projects']
collection_project_docs = db['documents']
# Refresh token


EMIT_PROJECTS_UPDATE = 'PROJECTS'
EMIT_VENDORS_UPDATE = 'VENDORS'
EMIT_USERS_UPDATE = 'USERS'


def emitUpdate(type):
    requests.post('http://.0.0.1:5006/sendEmit', json={'update': type})
    return


@app.before_request
def log_request_info():
    # app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_json())


@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    # Set the access JWT and CSRF double submit protect ion cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200



@app.route('/users', methods=['GET', 'POST'])
@jwt_required
def users():
    if request.method == 'POST':
        body = request.get_json()
        try:
            if body['query'] == 'update_user_role':
                valid = validate_data(
                    body['data'], update_role_check_schema)
                if valid['ok']:
                    data = valid['data']
                    current_user = get_jwt_identity()
                    current_user_role = collection_user.find_one(
                        {"user_id": current_user}, projection={"admin": True, "_id": False})
                    if current_user_role.get('admin'):
                        user_id = data["user_id"]
                        query = {'user_id': user_id}
                        array = ["admin"]
                        update_required = {
                            "$set": {item: data[item] for item in array}}
                        update_user_data(
                            collection_user, query, update_required)
                        action = 'Updated user role'
                        add_action_user_admin(
                            collection_user, current_user, action, user_id)
                        message = 'User role updated successfully!'
                        #emitUpdate(EMIT_USERS_UPDATE)
                        return json_response(message, 200)
                    message = 'Unauthorised access'
                    return json_response(message, 400)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'update_self':
                valid = validate_data(
                    body['data'], user_check_schema)
                if valid['ok']:
                    data = valid['data']
                    current_user = get_jwt_identity()
                    query = {'user_id': current_user}
                    array = ["name", "designation",
                             "tech_stack", "projects"]
                    update_required = {
                        "$set": {item: data[item] for item in array}}
                    update_user_data(collection_user, query, update_required)
                    action = 'Updated user details'
                    add_action_user_self(collection_user, current_user, action)
                    message = 'User data updated successfully!'
                    #emitUpdate(EMIT_USERS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'update_user':
                # admin only
                current_user = get_jwt_identity()
                current_user_role = collection_user.find_one(
                    {"user_id": current_user}, projection={"admin": True, "_id": False})

                if current_user_role.get('admin'):
                    valid = validate_data(
                        body['data'], user_check_schema_admin_update)

                    if valid['ok']:
                        data = valid['data']
                        user_id = data['user_id']
                        query = {'user_id': user_id}
                        array = ["name", "designation",
                                 "tech_stack", "projects"]
                        update_required = {
                            "$set": {item: data[item] for item in array}}
                        update_user_data(
                            collection_user, query, update_required)
                        action = 'Updated user details'
                        add_action_user_admin(
                            collection_user, current_user, action, user_id)
                        message = 'User data updated successfully!'
                        #emitUpdate(EMIT_USERS_UPDATE)
                        return json_response(message, 200)
                    message = valid['message']
                    return json_response(message, 400)
                message = "Only admin can update"
                return json_response(message, 400)
            if body['query'] == 'delete_user':
                # admin only
                current_user = get_jwt_identity()
                current_user_role = collection_user.find_one(
                    {"user_id": current_user}, projection={"admin": True, "_id": False})

                if current_user_role.get('admin'):
                    valid = validate_data(
                        body['data'], delete_user_check_schema)
                    if valid['ok']:
                        data = valid['data']
                        user = data['user_id'] 
                        query = {'user_id': user}
                        delete_user(collection_user, query)
                        message = 'User deleted successfully!'
                        action = 'Deleted a user'
                        add_action_user_admin(
                            collection_user, current_user, action, user)
                        #emitUpdate(EMIT_USERS_UPDATE)
                        return json_response(message, 200)
                    message = valid['message']
                    return json_response(message, 400)
                message = "Only admin can delete user"
                return json_response(message, 400)
            if body['query'] == 'update_password':
                valid = validate_data(
                    body['data'], user_change_password_check_schema)
                if valid['ok']:
                    data = valid['data']
                    current_user = get_jwt_identity()
                    current_user_details = collection_user.find_one(
                        {'user_id': current_user})
                    if not flask_bcrypt.check_password_hash(current_user_details['password'], data['old_password']):
                        message = 'Current password is wrong'
                        return json_response(message, 400)
                    query = {'user_id': current_user}
                    array = ["password"]
                    new_password = flask_bcrypt.generate_password_hash(
                        data['new_password']).decode('utf-8')
                    update_required = {
                        "$set": {'password': new_password}}
                    update_user_data(collection_user, query, update_required)
                    action = 'Password updated'
                    add_action_user_self(collection_user, current_user, action)
                    message = 'Password updated successfully!'
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
        except Exception as e:
            return bad_request(str(e))
    if request.method == 'GET':
        try:
            arguments = request.args.to_dict()
            if arguments.get('get_all_users'):
                current_user = get_jwt_identity()
                current_user_role = collection_user.find_one(
                    {"user_id": current_user}, projection={"admin": True, })
                if current_user_role.get('admin'):

                    response = get_all_users(collection_user)
                    message = 'Users fetched successfully'
                    return json_response(message, 200, {"users": response})
                else:
                    projection = {"_id": False, "session_trail": False,
                                  "action_trail": False, "last_logged_in": False, 'password': False}
                    response = get_all_users(collection_user, projection)
                    message = 'Users fetched successfully'
                    return json_response(message, 200, {"users": response})
            else:
                current_user = get_jwt_identity()
                user_data = get_user_data(
                    collection_user, {"user_id": current_user})
                message = 'User fetched successfully'
                return json_response(message, 200, {"user_data": user_data})
        except Exception as e:
            return bad_request(str(e))


@app.route('/register', methods=['POST'])
@jwt_required
def register():
    body = request.get_json()
    try:
        current_user = get_jwt_identity()
        print(current_user)
        current_user_role = collection_user.find_one(
            {"user_id": current_user}, projection={"admin": True, })
        if current_user_role.get('admin'):
            data = validate_data(body['data'], user_register_check_schema)
            if data['ok']:
                data = data['data']
                user = collection_user.find_one({'email': data['email']})
                if user:
                    message = 'User already registered'
                    return json_response(message, 400)
                    # return json_response.user_registration(True)
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password']).decode('utf-8')
                data['user_id'] = str(uuid.uuid4())
                user = user_profile_schema(data)
                collection_user.insert_one(user)
                message = 'Registration successfull'
                #emitUpdate(EMIT_USERS_UPDATE)
                return json_response(message, 200)
            message = 'Registration failed'
            return json_response(message, 400)
        message = 'Only admin can add users'
        return json_response(message, 400)
    except Exception as e:
        return bad_request()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # collection_items.remove({})
    # collection_user.remove({})
    if request.method == 'POST':
        body = request.get_json()
        try:
            data = validate_data(body['data'], user_login_check_schema)
            if data['ok']:
                data = data['data']
                user = collection_user.find_one({'email': data['email']})
                if not user:
                    message = 'User not registered'
                    return json_response(message, 400)
                print('printing user')
                print(user)
                if flask_bcrypt.check_password_hash(user['password'], data['password']):
                    access_token = create_access_token(
                        identity=user['user_id'])
                    print('passed')
                    refresh_token = create_refresh_token(
                        identity=user['user_id'])
                    response = jsonify({'Login': True ,})
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)
                    del user['_id']
                    nowtime = current_time()
                    object = {"logged_in": True, "time": nowtime}
                    data = {
                        "$push": {"session_trail": object}}
                    collection_user.find_one_and_update({"user_id": user['user_id']}, {
                        "$set": {"last_logged_in": nowtime}, "$push": {"session_trail": object}}, upsert=True)
                    return response, 200
                else :
                     message = 'Error wrong password'
                     return json_response(message, 400)
            message = 'Invalid data sent to server'
            return json_response(message, 400)
        except Exception as e:
            print(e)
            return bad_request()
    message = 'Only POST method allowed'
    return json_response(message, 400)


@app.route('/logout', methods=['GET'])
@jwt_required
def Logout():
    # collection_items.remove({})
    # collection_user.remove({})
    if request.method == 'GET':
        # body = request.get_json()
        try:
            current_user = get_jwt_identity()
            nowtime = current_time()
            object = {"logged_out": True, "time": nowtime}
            collection_user.find_one_and_update({"user_id": current_user}, {
                "$push": {"session_trail": object}}, upsert=True)
            access_token = create_access_token(identity='None')
            response = jsonify({'Logout': True})
            set_access_cookies(response, access_token, max_age=-1)
            #emitUpdate(EMIT_USERS_UPDATE)
            return response, 200
        except Exception as e:
            return bad_request()
    message = 'Only POST method allowed'
    return json_response(message, 400)


@app.route('/employee', methods=['GET', 'POST'])
@jwt_required
def vendors():
    if request.method == 'POST':
        body = request.get_json()
        try:
            if body['query'] == 'add_employee':
                valid = validate_data(
                    body['data'], employee_profile_check_schema)
                if valid['ok']:
                    data = body['data']
                    current_user = get_jwt_identity()
                    data['author_id'] = current_user
                    item_id = str(uuid.uuid4())
                    data['item_id'] = item_id
                    post = employee_profile_schema(data)
                    add_new_vendor(collection_vendors, post)
                    action = 'Added new vendor'
                    add_action_user_vendor(
                        collection_user, current_user, action, item_id)
                    message = 'Vendor added successfully!'
                    #emitUpdate(EMIT_VENDORS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'update_vendor':
                valid = validate_data(
                    body['data'], employee_profile_check_schema)
                if valid['ok']:
                    data = body['data']
                    current_user = get_jwt_identity()
                    data['author_id'] = current_user
                    item_id = data['item_id']
                    query = {'item_id': item_id}
                    array = ["basic_details", "empanelment_details",
                             "work_profile", "project_details"]
                    update_required = {
                        "$set": {item: data[item] for item in array}}
                    update_vendor_data(collection_vendors,
                                       query, update_required)
                    action = 'Updated a vendor'
                    add_action_user_vendor(
                        collection_user, current_user, action, item_id)
                    message = 'Vendor updated successfully!'
                    #emitUpdate(EMIT_VENDORS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
        except Exception as e:
            return bad_request()
    if request.method == 'GET':
        arguments = request.args.to_dict()
        try:
            if arguments:
                search_query = arguments['search']
                array = get_vendor(collection_vendors,
                                   query={"basic_details.vendor_name": {"$regex": "^" + search_query, "$options": 'i'}}, projection={"_id": False, "basic_details.vendor_name": True, "item_id": True})
                message = 'Successfully completed search query'
                return json_response(message, 200, {"vendors": array})
            else:
                array = get_all_vendors(collection_vendors)
                message = 'Vendors fetched successfully'
                return json_response(message, 200, {"vendors": array})
        except Exception as e:
            return bad_request(str(e))


@app.route('/projects', methods=['GET', 'POST'])
@jwt_required
def projects():
    if request.method == 'POST':
        body = request.get_json()
        try:
            if body['query'] == 'add_project':
                valid = validate_data(
                    body['data'], project_profile_check_schema)
                if valid['ok']:
                    data = valid['data']
                    current_user = get_jwt_identity()
                    temp_name = data['basic_details']['project_name'].split()
                    data['project_id'] = temp_name[0] + \
                        '-' + str(randint(100000, 999999))
                    data['author_id'] = current_user
                    item_id = str(uuid.uuid4())
                    data['item_id'] = item_id
                    post = add_project_profile_schema(data)
                    #print(post)
                    #collection_projects.insert_one(post)
                    (add_new_project(collection_projects, post))
                    action = 'Added new project'
                    add_action_user_project(
                        collection_user, current_user, action, item_id)
                    #collection_projects.insert_one(post)
                    message = 'Project added successfully!'
                    #emitUpdate(EMIT_PROJECTS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'update_project':
                valid = validate_data(
                    body['data'], project_profile_check_schema)
                if valid['ok']:
                    data = body['data']
                    current_user = get_jwt_identity()
                    data['author_id'] = current_user
                    item_id = data['item_id']
                    query = {'item_id': item_id}
                    array = ["basic_details", "project_details",
                             "project_documents"]
                    update_required = {
                        "$set": {item: data[item] for item in array}}
                    update_project_data(collection_projects,
                                        query, update_required)
                    action = 'Updated a project'
                    add_action_user_project(
                        collection_user, current_user, action, item_id)
                    message = 'Project updated successfully!'
                    #emitUpdate(EMIT_PROJECTS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'add_cr':
                valid = validate_data(
                    body['data'], add_cr_check_schema)
                if valid['ok']:
                    data = body['data']
                    current_user = get_jwt_identity()
                    data['author_id'] = current_user
                    item_id = data['project_id']
                    stage_object = body['data']['change_request']
                    cr_id = str(uuid.uuid4())
                    nowtime = current_time()
                    object = {
                        **stage_object, 'cr_id': cr_id, "date_added": nowtime
                    }
                    collection_projects.find_one_and_update(
                        {"item_id": item_id}, {"$push": {"change_request": object}}, upsert=True)
                    action = 'Added a CR'
                    add_action_user_project(
                        collection_user, current_user, action, item_id)
                    message = 'CR added successfully!'
                    #emitUpdate(EMIT_PROJECTS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
            if body['query'] == 'update_cr':
                valid = validate_data(
                    body['data'], update_cr_check_schema)
                if valid['ok']:
                    data = body['data']
                    item_id = data['project_id']
                    cr_id = data['cr_id']
                    # query = {'item_id': item_id }
                    array = ["name", "stage"]
                    # stage_object = body['data']['change_request']
                    # cr_id = str(uuid.uuid4())
                    # object = {
                    #     **stage_object, 'cr_id': cr_id
                    # }
                    change_request = body['data']['change_request']
                    print(collection_projects.find_one({
                        "item_id": item_id,
                        "change_request.cr_id": cr_id
                    }))
                    collection_projects.find_one_and_update(
                        {"item_id": item_id, "change_request.cr_id": cr_id},
                        {"$set":

                         {"change_request.$." +
                             item: change_request[item] for item in array}

                         })
                    action = 'Updated a CR'
                    current_user = get_jwt_identity()
                    # data['author_id'] = current_user
                    add_action_user_project(
                        collection_user, current_user, action, item_id)
                    message = 'CR Updated successfully!'
                    #emitUpdate(EMIT_PROJECTS_UPDATE)
                    return json_response(message, 200)
                message = valid['message']
                return json_response(message, 400)
        except Exception as e:
            return bad_request(str(e))
    if request.method == 'GET':
        try:
            arguments = request.args.to_dict()
            if arguments:
                search_query = arguments['search']
                array = get_project(collection_projects,
                                    query={"basic_details.project_name": {"$regex": "^" + search_query, "$options": 'i'}}, projection={"_id": False, "basic_details.project_id": True, "basic_details.project_name": True, "item_id": True})
                message = 'Successfully completed search query'
                return json_response(message, 200, {"project": array})
            else:
                array = get_all_projects(collection_projects)
                message = 'Projects fetched successfully'
                return json_response(message, 200, {"projects": array})

        except Exception as e:
            return bad_request(str(e))

    return bad_request()



if __name__ == '__main__':
    # app.secret_key = args.appsecret
    ON_HEROKU = os.environ.get('ON_HEROKU')
    if ON_HEROKU:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        print('hello`')
        app.run(debug =True)
