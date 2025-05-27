from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ItemInDBBase(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True  # В реальном проекте orm_mode теперь from_attributes


class Item(ItemInDBBase):
    pass


class ItemInDB(ItemInDBBase):
    pass
