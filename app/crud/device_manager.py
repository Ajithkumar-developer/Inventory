from ..utils.logger import get_logger
from ..utils.stock_calculator import StockCalculatorService
from ..db.base.database_manager import DatabaseManager
from ..models.device_model import Device
from ..schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DeviceRead,
    BatteryUpdate,
    LocationUpdate,
    TrackingUpdate
)

logger = get_logger(__name__)


class DeviceManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)
        self.stock_service = StockCalculatorService(db_type)

    # ------------------------
    # DEVICE CRUD
    # ------------------------

    async def create_device(self, device: DeviceCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(Device, device.dict())

            return {
                "success": True,
                "message": "Device created successfully",
                "data": DeviceRead.from_orm(obj).dict()
            }
        finally:
            await self.db_manager.disconnect()

    async def get_device(self, device_id: int) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(Device, {"DeviceId": device_id})

            if result:
                return {
                    "success": True,
                    "message": "Device fetched successfully",
                    "data": DeviceRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "Device not found", "data": None}
        finally:
            await self.db_manager.disconnect()

    async def get_all_devices(self) -> dict:
        try:
            await self.db_manager.connect()
            devices = await self.db_manager.read(Device)

            # Initialize status counters
            status_count = {
                "Online": 0,
                "Offline": 0,
                "Unlinked": 0,
                "LowBattery": 0
            }

            device_list = []

            for d in devices:
                # Count status safely
                if d.Status in status_count:
                    status_count[d.Status] += 1

                device_list.append(DeviceRead.from_orm(d).dict())

            return {
                "success": True,
                "message": "Devices fetched successfully",
                "data": {
                    **status_count,
                    "Devices": device_list
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching devices: {e}",
                "data": None
            }
        finally:
            await self.db_manager.disconnect()

    async def update_device(self, device_id: int, data: DeviceUpdate) -> dict:
        try:
            await self.db_manager.connect()

            rowcount = await self.db_manager.update(
                Device,
                {"DeviceId": device_id},
                data.dict(exclude_unset=True)
            )

            if rowcount:
                return {
                    "success": True,
                    "message": "Device updated successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Device not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_device(self, device_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Device, {"DeviceId": device_id})

            if rowcount:
                return {
                    "success": True,
                    "message": "Device deleted successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Device not found"}
        finally:
            await self.db_manager.disconnect()

    # ------------------------
    # DEVICE TRACKING
    # ------------------------

    async def update_device_weight(self, device_id: int, new_weight: float) -> dict:
        try:
            await self.db_manager.connect()

            # Fetch device first
            devices = await self.db_manager.read(Device, {"DeviceId": device_id})
            if not devices:
                return {
                    "success": False,
                    "message": "Device not found",
                    "data": None
                }

            device = devices[0]
            previous_weight = device.Weight  # Store old weight

            # ---------------------------
            # UPDATE DEVICE
            # ---------------------------
            await self.db_manager.update(
                Device,
                {"DeviceId": device_id},
                {
                    "LastReading": previous_weight,
                    "Weight": new_weight
                }
            )

            logger.info(
                f"Device {device_id} updated | "
                f"LastReading={previous_weight}, Weight={new_weight}"
            )

            # ---------------------------
            # TRIGGER STOCK RECALC
            # ---------------------------
            await self.stock_service.update_stock_by_device(device_id)

            return {
                "success": True,
                "message": "Device weight updated and stock recalculated",
                "data": {
                    "DeviceId": device_id,
                    "LastReading": previous_weight,
                    "Weight": new_weight
                }
            }

        except Exception as e:
            logger.error(f"Error updating device weight {device_id}: {e}")
            return {
                "success": False,
                "message": f"Error updating device weight: {e}",
                "data": None
            }

        finally:
            await self.db_manager.disconnect()

    async def sync_device(self, device_id: int) -> dict:
        return {
            "success": True,
            "message": "Device synced successfully",
            "data": {"DeviceId": device_id}
        }

    async def update_battery(self, device_id: int, data: BatteryUpdate) -> dict:
        return await self.update_device(device_id, BatteryUpdate(**data.dict()))

    async def update_location(self, device_id: int, data: LocationUpdate) -> dict:
        return await self.update_device(device_id, LocationUpdate(**data.dict()))

    async def update_tracking(self, device_id: int, data: TrackingUpdate) -> dict:
        return await self.update_device(device_id, TrackingUpdate(**data.dict()))

    async def get_tracking(self, device_id: int) -> dict:
        return await self.get_device(device_id)

    async def get_all_tracking(self) -> dict:
        return await self.get_all_devices()
