from fastapi import FastAPI, Request
from src.oauth import build_auth_url, exchange_code, refresh_access_token
from fastapi.responses import RedirectResponse
import time, secrets, os
from src.state import tokens_store
from dotenv import load_dotenv
from src.state import get_access_token
from src.fetcher.mal import get_mal_list
from src.llm import generate_prompt, call_llm
load_dotenv()


app = FastAPI()


redirect_uri = os.getenv("REDIRECT_URI")
mal_auth_url = os.getenv("MAL_AUTH")
mal_token_url = os.getenv("MAL_TOKEN")


@app.get("/login")
def login():
    state = secrets.token_urlsafe(16)
    auth_url = build_auth_url(redirect_uri, state, mal_auth_url)
    return RedirectResponse(auth_url)


@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    tokens = exchange_code(code, redirect_uri, state, mal_token_url)

    tokens_store[state] = {
        "access": tokens["access_token"],
        "refresh": tokens["refresh_token"],
        "expires_at": time.time() + tokens["expires_in"]
    }
   
    return {
        "message": "auth success",
        "state" : state,
        "token" : tokens["access_token"]
    }
    

@app.get("/analyse")
def analyse(state:str):
    access_token = get_access_token(state)
    mal_user_data = get_mal_list(access_token)
    print(mal_user_data)
    prompt = generate_prompt(mal_user_data)
    result = call_llm(prompt)

    return {result: result}