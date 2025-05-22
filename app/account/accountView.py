from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.main import db

from app.main import decodeJWT, JWT_SECRET,JWT_ALGORITHM
from db.postgresql import get_db
from .accountModel import AccountUser
from .accountSchema import UserRegistrationSchema, UserLoginSchema

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

router = APIRouter(prefix="/v1/account", tags=["Account"])

@router.post("/register")
def register_user(user: UserRegistrationSchema, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    existing_user = db.query(AccountUser).filter((AccountUser.email == user.email) | (AccountUser.phone == user.phone)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or phone number already exists")

    hashed_password = get_password_hash(user.password)
    new_user = AccountUser(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"},200

@router.post("/login")
def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(AccountUser).filter((AccountUser.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email or db_user.phone}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}