def add_new_project(coll, data, projection={"_id": False}):

    coll.insert_one(data)
    return 


def add_new_project_doc(coll, data):
    coll.insert_one(data)
    return


def get_all_projects(coll, projection={"_id": False}):
    array = [project for project in coll.find({}, projection)]
    return array


def get_project(coll, query, projection={"_id": False}):
    array = [project for project in coll.find(query, projection)]
    return array


def update_project_data(coll, query, data, projection={"_id": False}):
    coll.update_one(query, data)
    return

def update_project_cr_data(coll, query, data, projection={"_id": False}):
    coll.update_one(query, data)
    return