import re
from flask import session, request, abort

valid_letters = r"[a-zA-ZåäöÅÄÖ]"

def require_login():
    if "user_id" not in session:
        abort(403)

def verify_csrf():
    if session.get("csrf_token") != request.form.get("csrf_token"):
        abort(403)

def validate_text(text):
    if not text or not re.search(valid_letters, text):
        return False
    return True

def validate_card_parameters(question, answer):
    if not question or not answer or len(question) > 60 or len(answer) > 60:
        return False
    if not validate_text(question) or not validate_text(answer):
        return False
    return True

def validate_deck_parameters(name, description):
    if not name or not description or len(name) > 30 or len(description) > 150:
        return False
    if not validate_text(name) or not validate_text(description):
        return False
    return True