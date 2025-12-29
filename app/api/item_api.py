from fastapi import APIRouter, HTTPException
from ..config import settings
from ..crud.item_manager import ItemManager
from ..schemas.item_schema import ItemCreate, ItemUpdate


class ItemAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = ItemManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/items")(self.create_item)
        self.router.get("/items")(self.get_all_items)
        self.router.get("/items/{item_id}")(self.get_item)
        self.router.put("/items/{item_id}")(self.update_item)
        self.router.delete("/items/{item_id}")(self.delete_item)

    async def create_item(self, item: ItemCreate):
        return await self.manager.create_item(item)

    async def get_all_items(self):
        return await self.manager.get_all_items()

    async def get_item(self, item_id: int):
        return await self.manager.get_item(item_id)

    async def update_item(self, item_id: int, item: ItemUpdate):
        return await self.manager.update_item(item_id, item)

    async def delete_item(self, item_id: int):
        return await self.manager.delete_item(item_id)
