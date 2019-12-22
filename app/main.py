from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException
import uvicorn

from app.routers import items, users
from app.database import engine

from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

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



async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)