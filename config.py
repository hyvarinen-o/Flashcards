import secrets
secret_key = "5085cd0f92a62ecd315ada45ecd6614e"

def generate_csrf_token():
    return secrets.token_hex(16)