import base64
import secrets
import hashlib


def generate_code_verifier():
    return secrets.token_urlsafe(64)

def generate_code_challenge(verifier :str):
    return verifier