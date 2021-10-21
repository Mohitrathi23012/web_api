from pymongo.helpers import _index_list
from current_time import current_time


def project_details_schema(data):
    return {
        "name": data['name'],
        "designation": data['designation'],
        "contact": data['contact']
        }
    
def CR_schema(data):
    return {
        "work_order": data['work_order'],
        "milestone_report": data['milestone_report'],
        "invoices": data['invoices'],
        "emails": data['emails'],
        "other_docs": data['other_docs']
    }
def project_profile_schema(data):
    nowtime = current_time()
    project_id = data['project_id']
    basic_detials = data['basic_details']
    project_details = data['project_details']
    project_documents = data['project_documents']
    project_profile ={
        "basic_details":{
            "project_name": basic_detials['project_name'],
            "team":basic_detials['team'],
            "summary":basic_detials['summary'],
            "project_link":basic_detials['project_link'],
            "project_cost":basic_detials['project_cost']
        },
        "project_details":{
            "project_team_leader":project_details_schema(project_details['project_team_leader']),
            "it_team":project_details_schema(project_details['it_team'])
        },
        "project_documents": {
            "work_order": project_documents['work_order'],
            "milestone_report": project_documents['milestone_report'],
            "invoices": project_documents['invoices'],
            "emails": project_documents['emails'],
            "other_docs": project_documents['other_docs'],

        },
        "item_id":data['item_id'],
        "author_id":data['author_id'],
        "date_added":nowtime
    }

    return project_profile
def add_project_profile_schema(data):
    nowtime = current_time()
    project_id = data['project_id']
    basic_details = data['basic_details']
    project_details = data['project_details']
    project_profile = {
        "basic_details": {
            "project_id": project_id,
            "project_name": basic_details['project_name'],
            "summary": basic_details['summary'],
            "project_link": basic_details['project_link'],
            "project_value_inr": basic_details['project_value_inr']

        },
        "project_details": {
            "project_team_leader": project_details_schema(project_details['project_team_leader']),
            "it_team":project_details_schema(project_details['it_team'])
        },
        "item_id": data['item_id'],
        "author_id": data['author_id'],
        "date_added": nowtime
    }
    return project_profile

