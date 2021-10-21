import datetime

def current_time():
    return datetime.datetime.utcnow().isoformat() + 'Z'
