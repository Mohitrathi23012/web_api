from current_time import current_time

def get_all_users(coll, projection={"_id": False, 'password': False}):
    array = [user for user in coll.find({}, projection)]
    return array


def get_user_data(coll, query, projection={"_id": False, 'password': False}):
    array = [user for user in coll.find(query, projection)]
    return array


def update_user_data(coll, query, data, projection={"_id": False}):
    coll.update_one(query, data)
    return

def delete_user(coll, query):
    coll.delete_one(query)
    return

def add_action_user_vendor(coll, user_id,query, object_id):
    nowtime = current_time()
    object = {
        "action": query,
        "time": nowtime,   
        'vendor': True,
        'object_id': object_id
    }
    coll.find_one_and_update({"user_id": user_id}, {"$push": {"action_trail": object}}, upsert=True)
    return

def add_action_user_project(coll, user_id,query, object_id):
    nowtime = current_time()
    object = {
        "action": query,
        "time": nowtime,   
        'project': True,
        'object_id': object_id
    }
    coll.find_one_and_update({"user_id": user_id}, {"$push": {"action_trail": object}}, upsert=True)
    return


def add_action_user_admin(coll, self_user_id, query, other_user_id):
    nowtime = current_time()
    object = {
        "action": query,
        "time": nowtime,   
        'self': False,
        'object_id': other_user_id
    }
    coll.find_one_and_update({"user_id": self_user_id}, {"$push": {"action_trail": object}}, upsert=True)
    return

def add_action_user_self(coll, self_user_id, query):
    nowtime = current_time()
    object = {
        "action": query,
        "time": nowtime,   
        'self': True,
    }
    coll.find_one_and_update({"user_id": self_user_id}, {"$push": {"action_trail": object}}, upsert=True)
    return 