from database.project_profile_schema import add_project_profile_schema


project_profile_check_schema ={
    "type":"object",
    "properties":{
        "basic_details":{
            "type":"object",
            "properties":{
                "project_name":{"type":"string"},
                "team" :{"type":"string"},
                "summary":{"type":"string"},
                "project_link":{"type":"string"},
                "project_value":{"type":"string"}
            }
        },
        "project_details":{
            "type":"object",
            "properties":{
                "project_team_leader":{
                    "type":"object",
                    "properties":{
                        "name":{"type":"string"},
                        "desingation":{"type":"string"},
                        "contact":{"type":"string"}
                    }
                },
                "it_team":{
                    "type":"object",
                    "properties":{
                        "name":{"type":"string"},
                        "desingation":{"type":"string"},
                        "contact":{"type":"string"}
                    }
                },
        }
    },
    "documents":{
        "type":"object",
        "properties": {
            "work_order": {"type": "array"},
            "milestone_report": {"type": "array"},
            "invoices": {"type": "array"},
            "emails": {"type": "array"},
            "other_docs": {"type": "array"},
            "change_request": {
                "type": "object",
                "properties": {
                    "work_order": {"type": "array"},
                    "milestone_report": {"type": "array"},
                    "invoices": {"type": "array"},
                    "emails": {"type": "array"},
                    "other_docs": {"type": "array"},
                    }
            },
        }
    },
    "additionalProperties": True
    }
}
add_project_check_schema = {
    "type": "object",
    "properties": {
        "project_stage": {
            "type": "object",
            "properties": {
                "stage": {"type": "string"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
            }
        }
    },
    "additionalProperties": True
},
add_cr_check_schema = {
    "type": "object",
    "properties": {
        "change_request": {
            "type": "object",
            "properties": {
                "name": {"type": "string",},
                "stage": {"type": "array"},
                "documents" :{"type": "array"}
            }
        },
        "project_id": {
            "type": "string",
        }
    },
    "additionalProperties": True
},

update_cr_check_schema = {
    "type": "object",
    "properties": {
        "change_request": {
            "type": "object",
            "properties": {
                "name": {"type": "string",},
                "stage": {"type": "array"},
            }
        },
        "cr_id": {
            "type": "string",
        },
        "project_id": {"type": "string"}
    },
    "additionalProperties": False
}