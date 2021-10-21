

employee_profile_check_schema = {
    "type": "object",
    "properties": {
        "basic_details": {
            "type": "object",
            "properties": {
                "employee_name": {"$ref": "#/definitions/non-empty-string"},
                "address": {"type": "string"},
                "summary":{"type":"string"},
                "contact_number": {"type": "string"},
                "designation": {"type": "string"},
                "contact_number_kcp": {"type": "string"},
                "email_address": {"type": "string"},
                "employee_website": {"type": "string"}
            }
        },
        "work_profile": {
            "type": "object",
            "properties": {
                "servies_offered": {"type": "array"},
                "types_of_projects": {"type": "array"},
                "govt_bodies_worked_on": {"type": "array"},
                "tech_proficiency": {"type": "array"},
            }

        },
        "project_details": {
            "type": "object",
            "properties": {
                "projects_working_on": {"type": "array"},
            }
        },
        "item_id": {
            "type": "string"
        }
    },
    "definitions": {
        "non-empty-string": {
            "type": "string",
            "minLength": 1
        }
    },
    "additionalProperties": False
}
