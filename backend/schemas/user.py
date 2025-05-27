from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8,
                          description="Пароль должен содержать минимум 8 символов")
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserProfileCreate(BaseModel):
    age: Optional[int] = Field(
        None, ge=16, le=100, description="Возраст от 16 до 100 лет")
    financial_experience: str = Field(...,
                                      description="Уровень финансового опыта")
    monthly_income: Optional[float] = Field(
        None, ge=0, description="Ежемесячный доход")
    financial_goals: Optional[List[str]] = Field(
        default_factory=list, description="Финансовые цели")
    risk_tolerance: Optional[str] = Field(
        None, description="Толерантность к риску")
    preferred_learning_style: Optional[str] = Field(
        None, description="Предпочитаемый стиль обучения")
    goals: Optional[str] = Field(None, description="Дополнительные цели")


class UserProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=16, le=100)
    financial_experience: Optional[str] = None
    monthly_income: Optional[float] = Field(None, ge=0)
    financial_goals: Optional[List[str]] = None
    risk_tolerance: Optional[str] = None
    preferred_learning_style: Optional[str] = None
    goals: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    financial_experience: Optional[str] = None
    monthly_income: Optional[float] = None
    financial_goals: Optional[List[str]] = None
    risk_tolerance: Optional[str] = None
    preferred_learning_style: Optional[str] = None
    goals: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithProfile(UserResponse):
    profile: Optional[UserProfileResponse] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True  # В реальном проекте orm_mode теперь from_attributes


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
