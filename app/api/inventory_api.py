from fastapi import APIRouter
from ..config import settings
from ..crud.inventory_manager import InventoryManager
from ..schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    StockUpdate,
    DeviceAssign
)


class InventoryAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = InventoryManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/inventory")(self.create_inventory)
        self.router.get("/inventory")(self.get_all_inventory)
        self.router.get("/inventory/{inventory_id}")(self.get_inventory)
        self.router.put("/inventory/{inventory_id}")(self.update_inventory)
        self.router.delete("/inventory/{inventory_id}")(self.delete_inventory)

        self.router.put("/inventory/{inventory_id}/update-stock")(self.update_stock)
        self.router.put("/inventory/{inventory_id}/assign-device")(self.assign_device)
        self.router.get("/inventory/device/{device_id}")(self.get_by_device)

    async def create_inventory(self, data: InventoryCreate):
        return await self.crud.create_inventory(data)

    async def get_inventory(self, inventory_id: int):
        return await self.crud.get_inventory(inventory_id)

    async def get_all_inventory(self):
        return await self.crud.get_all_inventory()

    async def update_inventory(self, inventory_id: int, data: InventoryUpdate):
        return await self.crud.update_inventory(inventory_id, data)

    async def delete_inventory(self, inventory_id: int):
        return await self.crud.delete_inventory(inventory_id)

    async def update_stock(self, inventory_id: int, data: StockUpdate):
        return await self.crud.update_stock(inventory_id, data)

    async def assign_device(self, inventory_id: int, data: DeviceAssign):
        return await self.crud.assign_device(inventory_id, data)

    async def get_by_device(self, device_id: int):
        return await self.crud.get_by_device(device_id)
