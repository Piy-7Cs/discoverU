from fastapi import FastAPI





app = FastAPI()


@app.get("/callback")
def callback():
    pass
