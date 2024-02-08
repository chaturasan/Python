import re
from schema import Schema, SchemaError, And, Use, Optional
import logging

EMAIL_REGEX_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

signup_schema = Schema({
    'email': And(str, lambda s: len(s) >= 3 and re.match(EMAIL_REGEX_PATTERN, s), error='Invalid email format or too short'),
    'first_name': And(str, lambda s: len(s) >= 4, error='First name must be at least 4 characters long'),
    'password': And(str, lambda s: len(s) >= 8, error='Password must be at least 8 characters long'),
    'password_confirm': And(str, Use(str.lower), error='Password confirmation is required')
})

login_schema = Schema({
    'email': And(str, lambda s: len(s) >= 1 and re.match(EMAIL_REGEX_PATTERN, s), error='Not a valid Email'),
    'password': And(str, lambda s: len(s) >= 1, error='Password is required')
})

note_schema = Schema({
    'note':  And(str, lambda s: len(s) >= 1, error='Nothing was added in note')
})

def validate_signup_data(data):
    try:
        signup_schema.validate(data)
        if data.get('password') != data.get('password_confirm'): return False, "Password doesn't match"
        return True, None
    except SchemaError as e:
        return False, str(e)
 
    
def validate_login_data(data):
    try:
        login_schema.validate(data)
        return True, None
    except SchemaError as e:
        return False, str(e)
    

def validate_note_added(data):
    try:
        note_schema.validate(data)
        return True, None
    except SchemaError as e:
        return False, str(e)