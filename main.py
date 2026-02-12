
#Classes 

class AppError(Exception):
    def __init__(self, message: str):
        self.message = message



from fastapi import FastAPI, Request, HTTPException
from src.oauth import build_auth_url, exchange_code, refresh_access_token
from fastapi.responses import RedirectResponse, JSONResponse
import time, secrets, os
from dotenv import load_dotenv
from src.fetcher.mal import get_mal_list
from src.llm import generate_prompt, call_llm
from src.pkce import generate_code_challenge, generate_code_verifier
from src.redis_session import save_session, get_session, update_session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles





load_dotenv()

app = FastAPI()







redirect_uri = os.getenv("REDIRECT_URI")
mal_auth_url = os.getenv("MAL_AUTH")
mal_token_url = os.getenv("MAL_TOKEN")
prompt_pre = os.getenv("PROMPT_PREFIX")

@app.get("/login")
def login(request: Request):
    state = secrets.token_urlsafe(16)
    code_verifier = generate_code_verifier()

    auth_url = build_auth_url(redirect_uri, state, mal_auth_url, code_verifier)

    session_data = {"state": state,
                    "pkce_verifier": code_verifier}
    
    response =  RedirectResponse(auth_url)
    save_session(response, session_data)

    if not response: 
        raise AppError("No Response")
        

    return response


@app.get("/callback")
def callback(request: Request): 
    try:
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        session_data = get_session(request)
    
        if not session_data or state != session_data.get("state"):
            return RedirectResponse("/?logged_in=false")

        code_verifier = session_data.get("pkce_verifier")
        tokens = exchange_code(code, redirect_uri, state, mal_token_url, code_verifier)


    except Exception as e:
        raise AppError("Not Authenticated")
    
    session_data.update({
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "expires_at": time.time() + tokens['expires_in']
    })

    update_session(request, session_data)
    
    return RedirectResponse("/?logged_in=true")

@app.get("/analyse")
def analyse(request: Request):

    access_token = get_access_token(request)
    if not access_token:
        raise AppError("Session Not Found")

    mal_user_data = get_mal_list(access_token)
    if not mal_user_data :
        raise AppError("No Response")
    prompt = generate_prompt(prompt_pre, mal_user_data)
    
    result = call_llm(prompt)

    if result is None:
        raise AppError("No Response From LLM")

    return {
        "success" : True,
        "data": result.text}




@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=400,
        content={
            "success" : False,
            "error" : exc.message
        }
    )




app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")



#Functions



def get_access_token(request: Request):
    session_data = get_session(request)
    if not session_data.get("access_token"):
        raise AppError("Not Authenticated")
    
    if time.time() >= session_data.get("expires_at", 0):
        try:
            tokens = refresh_access_token(session_data.get("refresh_token"))
        except Exception as e:
            return None
        
        session_data.update({
            "access_token" : tokens["access_token"],
            "expires_at" : tokens["expires_at"]
        })
        
        if "refresh_token" in tokens:
            session_data["refresh_token"] = tokens["refresh_token"]

        update_session(request, session_data)
    session_data = get_session(request)

    return session_data.get("access_token")

