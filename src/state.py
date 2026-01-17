import time, os
from src.oauth import refresh_access_token, exchange_code
from dotenv import load_dotenv

load_dotenv()
mal_token = os.getenv("MAL_TOKEN")

tokens_store = {}


def get_access_token(state:str):
    token_info = tokens_store.get(state)
    if not token_info:
        raise Exception("No token for this user/State")
    
    if time.time() >= token_info["expires_at"]:
        tokens = refresh_access_token(token_info["refresh"])
        token_info["access"] = tokens["access_token"]
        token_info["expires_at"] = time.time() + tokens.get("expires_in", 3600)

        if "refresh_token" in tokens:
            token_info["refresh"] = tokens["refresh_token"]

        tokens_store[state] = token_info

    return token_info["access"]
