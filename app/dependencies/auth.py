from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
import jwt
from jwt import PyJWTError

from app.dependencies import get_db
from app.controllers.auth import oauth2_scheme, SECRET_KEY, ALGORITHM, get_account
from app.schemas.auth import TokenData


async def get_current_account(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id: str = payload.get("sub")
        if account_id is None:
            raise credentials_exception
        token_data = TokenData(account_id=account_id)
    except PyJWTError:
        raise credentials_exception
    account = get_account(db_session, id=token_data.account_id)
    if account is None:
        raise credentials_exception
    return account


# async def get_current_active_account(current_user: Account = Depends(get_current_account)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
