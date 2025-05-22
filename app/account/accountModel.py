from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field


class AccountUser(SQLModel, table=True):
    __tablename__ = 'account_user'

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    password: str = Field(nullable=False)
    phone: int = Field(nullable=False)