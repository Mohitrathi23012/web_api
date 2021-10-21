from current_time import current_time


def employee_profile_schema(data):
    nowtime = current_time()
    basic_details = data['basic_details']
    work_profile = data['work_profile']
    project_details = data['project_details']
    employee_profile = {
        "basic_details": {
            "employee_name": basic_details['vendor_name'],
            "address": basic_details['address'],
            "summary":basic_details['summary'],
            "contact_number": basic_details['contact_number'],
            "designation": basic_details['designation'],
            "contact_number": basic_details['contact_number'],
            "email_address": basic_details['email_address'],
            "employee_website": basic_details['employee_website']
        },
        "work_profile": {
            "servies_offered": work_profile['servies_offered'],
            "types_of_projects": work_profile['types_of_projects'],
            "tech_proficiency": work_profile['tech_proficiency'],

        }, "project_details": {
            "projects_working_on": project_details['projects_working_on'],
        },
        "item_id": data['item_id'],
        "author_id": data['author_id'],
        "date_added": nowtime
    }

    return employee_profile
