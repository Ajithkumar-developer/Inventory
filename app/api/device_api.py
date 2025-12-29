from fastapi import APIRouter
from ..config import settings
from ..crud.device_manager import DeviceManager
from ..schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    BatteryUpdate,
    LocationUpdate,
    TrackingUpdate
)


class DeviceAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = DeviceManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        # Device CRUD
        self.router.post("/devices")(self.create_device)
        self.router.get("/devices")(self.get_all_devices)
        self.router.get("/devices/tracking")(self.get_all_tracking)
        self.router.get("/devices/{device_id}")(self.get_device)
        self.router.put("/devices/{device_id}")(self.update_device)
        self.router.delete("/devices/{device_id}")(self.delete_device)
        

        # Device Tracking
        self.router.get("/devices/{device_id}/sync")(self.sync_device)
        # self.router.put("/devices/{device_id}/weight")(self.update_device_weight)
        self.router.put("/devices/{device_id}/battery")(self.update_battery)
        self.router.put("/devices/{device_id}/location")(self.update_location)
        self.router.put("/devices/{device_id}/tracking")(self.update_tracking)
        self.router.get("/devices/{device_id}/tracking")(self.get_tracking)

    # -------- Device --------

    async def create_device(self, device: DeviceCreate):
        return await self.crud.create_device(device)

    async def get_device(self, device_id: int):
        return await self.crud.get_device(device_id)

    async def get_all_devices(self):
        return await self.crud.get_all_devices()

    async def update_device(self, device_id: int, device: DeviceUpdate):
        return await self.crud.update_device(device_id, device)

    async def delete_device(self, device_id: int):
        return await self.crud.delete_device(device_id)

    # -------- Tracking --------
    async def update_device_weight(self,device_id: int, new_weight: float):
        return await self.crud.update_device_weight(device_id=device_id,new_weight=new_weight)
        
    async def sync_device(self, device_id: int):
        return await self.crud.sync_device(device_id)

    async def update_battery(self, device_id: int, data: BatteryUpdate):
        return await self.crud.update_battery(device_id, data)

    async def update_location(self, device_id: int, data: LocationUpdate):
        return await self.crud.update_location(device_id, data)

    async def update_tracking(self, device_id: int, data: TrackingUpdate):
        return await self.crud.update_tracking(device_id, data)

    async def get_tracking(self, device_id: int):
        return await self.crud.get_tracking(device_id)

    async def get_all_tracking(self):
        return await self.crud.get_all_tracking()



