from fastapi import APIRouter
from ..config import settings
from ..crud.device_manager import DeviceManager, WeightTrackingManager, ActivityLogManager
from ..schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    BatteryUpdate,
    LocationUpdate,
    TrackingUpdate,
    WeightTrackingCreate,
    ActivityLogCreate
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
        self.router.put("/devices/{device_id}/weight")(self.update_device_weight)
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