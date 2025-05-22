from fastapi import FastAPI
from config import engine,create_db_and_tables
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from fastapi import Depends, status
from config import database

JWT_ALGORITHM = "HS256"
JWT_SECRET = "Shri@123"

app = FastAPI(title="ChatWeaver API")

db = engine

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This class will provide bearer authentication.
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        return True 

def decodeJWT(token: str= Depends(JWTBearer())):
    try:
        decodedToken = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decodedToken
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid authorization code"
        )
    

def create_app():
    # create_db_and_tables()
    from app.account import accountView
    app.include_router(accountView.router)

    from app.chat import chatView
    app.include_router(chatView.router)
    return app