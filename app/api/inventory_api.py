from fastapi import APIRouter
from ..config import settings
from ..crud.inventory_manager import InventoryManager, WeightTrackingManager, ActivityLogManager
from ..schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryWeightUpdate,
    WeightTrackingCreate,
    ActivityLogCreate
)


class InventoryAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = InventoryManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/inventory")(self.create_inventory)
        self.router.get("/inventory")(self.get_all_inventory)
        self.router.get("/inventory/info")(self.get_all_inventory_info)
        self.router.get("/inventory/info/{inventory_id}")(self.get_inventory_info)
        self.router.get("/inventory/{inventory_id}")(self.get_inventory)
        self.router.put("/inventory/{inventory_id}")(self.update_inventory)
        self.router.delete("/inventory/{inventory_id}")(self.delete_inventory)

        self.router.put("/inventory/{device_id}/update-weight")(
            self.update_weight_by_device
        )

    async def create_inventory(self, data: InventoryCreate):
        return await self.manager.create_inventory(data)

    async def get_all_inventory(self):
        return await self.manager.get_all_inventory()

    async def get_inventory(self, inventory_id: int):
        return await self.manager.get_inventory(inventory_id)

    async def update_inventory(self, inventory_id: int, data: InventoryUpdate):
        return await self.manager.update_inventory(inventory_id, data)

    async def delete_inventory(self, inventory_id: int):
        return await self.manager.delete_inventory(inventory_id)

    async def update_weight_by_device(
        self, device_id: int, weight: float
    ):
        return await self.manager.update_weight_by_device(
            device_id, weight
        )
    
    async def get_all_inventory_info(self):
        return await self.manager.get_inventory_info()

    async def get_inventory_info(self, inventory_id: int):
        return await self.manager.get_inventory_info_by_id(inventory_id)





class WeightTrackingAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = WeightTrackingManager(settings.db_type)
        self._routes()

    def _routes(self):
        self.router.post("/device/{device_id}/weight-tracking")(self.create)
        self.router.get("/device/{device_id}/weight-tracking")(self.get)
        self.router.delete("/device/{device_id}/weight-tracking")(self.delete)
        self.router.delete("/device/weight-tracking")(self.clear)

    async def create(self, device_id: int, payload: WeightTrackingCreate):
        return await self.manager.create(device_id, payload.Weight)

    async def get(self, device_id: int, filter: str = None):
        data = await self.manager.get(device_id, filter)
        return {"success": True, "data": data}

    async def delete(self, device_id: int):
        rows = await self.manager.delete_by_device(device_id)
        return {"success": True, "deleted": rows}

    async def clear(self):
        await self.manager.clear()
        return {"success": True, "message": "Weight tracking cleared"}
    


class ActivityLogAPI:
    def __init__(self):
        self.router = APIRouter()
        self.manager = ActivityLogManager(settings.db_type)
        self._routes()

    def _routes(self):
        self.router.post("/device/{device_id}/activity-tracking")(self.create)
        self.router.get("/device/{device_id}/activity-tracking")(self.get)
        self.router.delete("/device/{device_id}/activity-tracking")(self.delete)
        self.router.delete("/device/activity-tracking")(self.clear)

    async def create(self, device_id: int, payload: ActivityLogCreate):
        return await self.manager.create(device_id, payload.Event)

    async def get(self, device_id: int, filter: str = None):
        data = await self.manager.get(device_id, filter)
        return {"success": True, "data": data}

    async def delete(self, device_id: int):
        rows = await self.manager.delete_by_device(device_id)
        return {"success": True, "deleted": rows}

    async def clear(self):
        await self.manager.clear()
        return {"success": True, "message": "Activity log cleared"}





# from fastapi import APIRouter
# from ..config import settings
# from ..crud.inventory_manager import InventoryManager
# from ..schemas.inventory_schema import (
#     InventoryCreate,
#     InventoryUpdate,
#     StockUpdate,
#     DeviceAssign
# )


# class InventoryAPI:
#     def __init__(self):
#         self.router = APIRouter()
#         self.crud = InventoryManager(settings.db_type)
#         self.register_routes()

#     def register_routes(self):
#         self.router.post("/inventory")(self.create_inventory)
#         self.router.get("/inventory")(self.get_all_inventory)
#         self.router.get("/inventory/{inventory_id}")(self.get_inventory)
#         self.router.put("/inventory/{inventory_id}")(self.update_inventory)
#         self.router.delete("/inventory/{inventory_id}")(self.delete_inventory)

#         self.router.put("/inventory/{inventory_id}/update-stock")(self.update_stock)
#         self.router.put("/inventory/{inventory_id}/assign-device")(self.assign_device)
#         self.router.get("/inventory/device/{device_id}")(self.get_by_device)

#     async def create_inventory(self, data: InventoryCreate):
#         return await self.crud.create_inventory(data)

#     async def get_inventory(self, inventory_id: int):
#         return await self.crud.get_inventory(inventory_id)

#     async def get_all_inventory(self):
#         return await self.crud.get_all_inventory()

#     async def update_inventory(self, inventory_id: int, data: InventoryUpdate):
#         return await self.crud.update_inventory(inventory_id, data)

#     async def delete_inventory(self, inventory_id: int):
#         return await self.crud.delete_inventory(inventory_id)

#     async def update_stock(self, inventory_id: int, data: StockUpdate):
#         return await self.crud.update_stock(inventory_id, data)

#     async def assign_device(self, inventory_id: int, data: DeviceAssign):
#         return await self.crud.assign_device(inventory_id, data)

#     async def get_by_device(self, device_id: int):
#         return await self.crud.get_by_device(device_id)
