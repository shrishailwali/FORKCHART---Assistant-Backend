from pydantic import BaseModel, EmailStr, Field

class UserRegistrationSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: int | None = None
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567",
                "password": "password123",
                "confirm_password": "password123",
                "username": "johndoe"
            }
        }

class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "password123"
            }
        }