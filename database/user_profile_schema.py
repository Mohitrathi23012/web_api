from current_time import current_time


def user_profile_schema(data):
    nowtime = current_time()

    user_profile_item = {
        "email": data['email'],
        "password": data['password'],
        "user_id": data['user_id'],
        "name": data['name'],
        "last_logged_in": "",
        "designation": "",
        "tech_stack": [],
        "projects": [],
        "session_trail": [],
        "action_trail": [],
        "admin" : False,
        "date_added": nowtime
    }

    # user_profile_item = {
    #     "user_email": data['user_email'],
    #     "user_id": data['user_id'],
    #     "name": data['name'],
    #     "designation": data['designation'],
    #     "tech_stack": data['tech_stack'],
    #     "projects": data['projects'],
    #     "session_trail": data['session_trail'],
    #     "action_trail": data['action_trail'],
    #     "user_role": data['user_role'],
    #     "date_added": nowtime
    # }

    return user_profile_item
