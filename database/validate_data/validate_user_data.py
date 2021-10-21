
user_login_check_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["email",'password'],
    # "additionalProperties": False
}

user_register_check_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password":{
            "type": 'string'
        }
    },
    "required": ["email",'password'],
    "additionalProperties": False
}

reset_password_check_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        }
    },
    "required": ["email"],
    "additionalProperties": False
}

otp_check_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "OTP": {
            "type": "number"
        }
    },
    "required": ["OTP", "email"],
    "additionalProperties": False
}

user_check_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "designation": {"type": "string"},
        "tech_stack": {"type": "array"},
        "projects": {"type": "array"},
        # "session_trail": {"type": "array"},
        # "action_trail": {"type": "array"},
        "user_role": {"type": "string"},
    },
}
user_check_schema_admin_update = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "name": {"type": "string"},
        "designation": {"type": "string"},
        "tech_stack": {"type": "array"},
        "projects": {"type": "array"},
        # "session_trail": {"type": "array"},
        # "action_trail": {"type": "array"},
        "user_role": {"type": "string"},
    },
}
update_role_check_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "admin": {"type": "boolean"},
    },
}
delete_user_check_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
    },
}
user_change_password_check_schema = {
    "type": "object",
    "properties": {
        "old_password" : {"type": "string"},
        "new_password": {"type": "string"},
    },
}