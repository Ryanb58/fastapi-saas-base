from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException
import uvicorn

from app import crud, models, schemas
from app.auth import oauth2_scheme, UserInDB
from app.database import engine
from app.routers import items, users, auth

# Initialize Database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="My Super Project",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    docs_url="/docs", 
    redoc_url=None
)

@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)