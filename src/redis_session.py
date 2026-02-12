import redis
import pickle
import os
from fastapi import Request, Response


r = redis.Redis( host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), decode_responses=False)


SESSION_EXPIRE = 3600

def save_session(response: Response, data: dict, session_id : str = None):
    import secrets
    if not session_id: 
        session_id = secrets.token_urlsafe(32)
    r.setex(session_id, SESSION_EXPIRE, pickle.dumps(data)) 
    
    response.set_cookie( key="session_id", 
                         value=session_id,
                         max_age=SESSION_EXPIRE,
                         httponly=True,
                         samesite=None, 
                         secure=True)

def get_session(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {}
    data = r.get(session_id)
    if not data:
        return {}
    return pickle.loads(data)

def update_session(request: Request, data: dict):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    r.setex(session_id,SESSION_EXPIRE,pickle.dumps(data))
    return session_id


