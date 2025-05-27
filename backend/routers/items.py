from .users import PSEUDO_DB_USERS  # Импортируем "базу" пользователей
from fastapi import APIRouter, HTTPException, Depends
from typing import List

# Заглушки, как и в users.py
# from .. import schemas, crud
# from ..dependencies import get_db
# Используем наши псевдо-схемы
from ..schemas.item import Item, ItemCreate, ItemUpdate
from ..schemas.user import User  # Для информации о владельце

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

# Псевдо-база данных для предметов
PSEUDO_DB_ITEMS = []
ITEM_ID_COUNTER = 0

# Для связи с псевдо-пользователями (из users.py)
# В реальном приложении это была бы связь через БД


@router.post("/", response_model=Item)
async def create_item_for_user(item_in: ItemCreate, owner_id: int):  # Псевдо owner_id
    """
    Создать предмет для пользователя (псевдо).
    Предполагаем, что owner_id - это ID существующего пользователя.
    "
    global ITEM_ID_COUNTER
    # Проверим, существует ли такой пользователь (псевдо-проверка)
    owner_exists = any(u["id"] == owner_id for u in PSEUDO_DB_USERS)
    if not owner_exists:
        raise HTTPException(
            status_code=404, detail=f"Owner with id {owner_id} not found")

    ITEM_ID_COUNTER += 1
    db_item_data = {
        "id": ITEM_ID_COUNTER,
        "title": item_in.title,
        "description": item_in.description,
        "owner_id": owner_id
    }
    PSEUDO_DB_ITEMS.append(db_item_data.copy())
    return Item(**db_item_data)

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    """
    Получить список всех предметов(псевдо).
    "
    return [Item(**item_data) for item_data in PSEUDO_DB_ITEMS[skip: skip + limit]]


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    Получить предмет по ID (псевдо).
    "
    found_item_data = next(
        (item_data for item_data in PSEUDO_DB_ITEMS if item_data["id"] == item_id), None)
    if found_item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**found_item_data)

@router.put("/{item_id}", response_model=Item)
# Псевдо current_user_id
async def update_item(item_id: int, item_in: ItemUpdate, current_user_id: int = 0):
    """
    Обновить предмет(псевдо).
    В реальном приложении здесь была бы проверка, что current_user_id является владельцем.
    "
    item_idx = -1
    original_item_data = None
    for i, i_data in enumerate(PSEUDO_DB_ITEMS):
        if i_data["id"] == item_id:
            item_idx = i
            original_item_data = i_data
            break

    if item_idx == -1 or original_item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Псевдо-проверка прав (в реальном приложении current_user_id брался бы из токена)
    # if original_item_data["owner_id"] != current_user_id:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = item_in.model_dump(exclude_unset=True)
    PSEUDO_DB_ITEMS[item_idx].update(update_data)
    # Гарантируем, что owner_id не изменился через этот эндпоинт
    PSEUDO_DB_ITEMS[item_idx]["owner_id"] = original_item_data["owner_id"]
    return Item(**PSEUDO_DB_ITEMS[item_idx])


@router.delete("/{item_id}", response_model=Item)
async def delete_item(item_id: int, current_user_id: int = 0):  # Псевдо current_user_id
    """
    Удалить предмет (псевдо).
    В реальном приложении здесь была бы проверка, что current_user_id является владельцем.
    "
    item_idx = -1
    deleted_item_data = None
    for i, i_data in enumerate(PSEUDO_DB_ITEMS):
        if i_data["id"] == item_id:
            # Псевдо-проверка прав
            # if i_data["owner_id"] != current_user_id:
            #     raise HTTPException(status_code=403, detail="Not enough permissions")
            item_idx = i
            break
            
    if item_idx != -1:
        deleted_item_data = PSEUDO_DB_ITEMS.pop(item_idx)
    
    if deleted_item_data is None:
        # Либо не найден, либо (в реальном коде) нет прав
        raise HTTPException(status_code=404, detail="Item not found or not enough permissions")
    return Item(**deleted_item_data)
