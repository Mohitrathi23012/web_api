def add_new_vendor(coll, data, projection={"_id": False}):

    coll.insert_one(data)
    return


def get_all_vendors(coll, projection={"_id": False}):
    array = [vendor for vendor in coll.find({}, projection)]
    return array

def get_vendor(coll, query, projection={"_id": False}):
    array = [vendor for vendor in coll.find(query, projection)]
    return array

def update_vendor_data(coll, query, data, projection={"_id": False}):
    coll.update_one(query, data)
    return
