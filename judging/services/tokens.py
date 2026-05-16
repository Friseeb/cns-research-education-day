import secrets


def generate_judge_token(length=32):
    return secrets.token_urlsafe(length)[:length]
