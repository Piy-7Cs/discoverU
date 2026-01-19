import requests
import os
from dotenv import load_dotenv
from src.pkce import generate_code_challenge, generate_code_verifier
from urllib.parse import urlencode

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


pkce_store= {}


def build_auth_url(redirect_uri: str, state: str, AUTH_URL:str):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)


    pkce_store[state] = code_verifier

    params = {
        "response_type":"code",
        "client_id":client_id,
        "redirect_uri":redirect_uri,
        "state":state,
        "code_challenge":code_challenge,
        "code_challenge_method":"plain" 
    }

    req = requests.Request("GET", AUTH_URL, params=params).prepare()
    return req.url



from requests.auth import HTTPBasicAuth

def exchange_code(code: str, redirect_uri: str, state: str, TOKEN_URL:str):
    code_verifier = pkce_store.pop(state)

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(
        TOKEN_URL,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret),
    )

    return response.json()



def refresh_access_token(refresh_token, TOKEN_URL:str):
    
    data = {
        "grant_type":"refresh_token",
        "refresh_token":refresh_token
    }

    response = requests.post(TOKEN_URL, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()





