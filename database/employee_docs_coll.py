def add_new_vendor_doc(coll, data, projection={"_id": False}):
    doc = coll.insert_one(data)
    return doc


def get_vendor_doc(coll, query, projection={"_id": False}):
    array = [doc for doc in coll.find(query, projection)]
    return array
