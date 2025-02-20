import re
from datetime import datetime
from markupsafe import escape

def sanitizeString(string):
    if isinstance(string, str):
        return escape(string.strip())
    return None

def emailFormat(email):
    if isinstance(email, str):
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            return email
    return None

def phoneFormat(phone):
    phone = sanitizeString(phone);
    return re.sub(r"[^\d+]", "", phone) if phone else None

def dateFormat(date_str):
    try:
        data = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        date = datetime.strftime(data, "%Y-%m-%d %H:%M")
        return date
    except ValueError:
        return None
    
def nameFormat(name):
    if re.match("^[a-zA-Z][a-zA-Z' -]+(\s+[A-Za-z][a-zA-Z' -]+)?$", name):
        return name
    return None

def vehicleFormat(vehicle):
    if re.match(r"^[\w\d\.\-\'\s]+$", vehicle):
        return vehicle
    return None

def timeslotFormat(timeslot):
    timeslot = str.lower(timeslot)
    if timeslot == "mattino" or timeslot == "pomeriggio" or timeslot == "qualsiasi":
        return timeslot.capitalize()
    else:
        return None
    