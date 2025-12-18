from ..utils.logger import get_logger
from ..db.base.database_manager import DatabaseManager
from ..models.inventory_model import Inventory
from ..models.device_model import Device
from ..schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryRead,
    StockUpdate,
    DeviceAssign
)

logger = get_logger(__name__)


class InventoryManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # ------------------------
    # INVENTORY CRUD
    # ------------------------

    async def create_inventory(self, inv: InventoryCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(Inventory, inv.dict())

            return {
                "success": True,
                "message": "Inventory created successfully",
                "data": InventoryRead.from_orm(obj).dict()
            }
        finally:
            await self.db_manager.disconnect()

    async def get_inventory(self, inventory_id: int) -> dict:
        try:
            await self.db_manager.connect()

            inventories = await self.db_manager.read(
                Inventory,
                {"InventoryId": inventory_id}
            )

            if not inventories:
                return {
                    "success": False,
                    "message": "Inventory not found",
                    "data": None
                }

            inventory = inventories[0]

            device = None
            if inventory.DeviceId:
                devices = await self.db_manager.read(
                    Device,
                    {"DeviceId": inventory.DeviceId}
                )
                device = devices[0] if devices else None

            response_data = {
                "InventoryId": inventory.InventoryId,
                "ItemCode": inventory.ItemCode,
                "ItemName": inventory.ItemName,
                "Category": inventory.Category,
                "Description": inventory.Description,

                "Device": {
                    "DeviceId": device.DeviceId,
                    "DeviceName": device.DeviceName,
                    "LastReading": device.LastReading,
                    "Weight": device.Weight,
                    "LocationName": device.LocationName,
                } if device else None,

                "UnitWeight": inventory.UnitWeight,
                "Stock": inventory.Stock,
                "Threshold": inventory.Threshold,
                "StockOut": inventory.StockOut,
                "Consumption": inventory.Consumption,
                "Status": inventory.Status,
                "CreatedAt": inventory.CreatedAt,
                "UpdatedAt": inventory.UpdatedAt
            }

            return {
                "success": True,
                "message": "Inventory fetched successfully",
                "data": response_data
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching inventory: {e}",
                "data": None
            }

        finally:
            await self.db_manager.disconnect()


    async def get_all_inventory(self) -> dict:
        try:
            await self.db_manager.connect()

            inventories = await self.db_manager.read(Inventory)
            devices = await self.db_manager.read(Device)

            # Device lookup by DeviceId
            device_map = {d.DeviceId: d for d in devices}

            inventory_list = []

            total_items = 0
            low_stock = 0
            out_of_stock = 0
            linked_devices = 0

            for inv in inventories:
                total_items += 1

                stock = inv.Stock or 0
                status = inv.Status
                device = device_map.get(inv.DeviceId)

                # -------------------------
                # COUNTS BASED ON STORED STATUS
                # -------------------------
                if status == "LowStock":
                    low_stock += 1
                elif status == "OutOfStock":
                    out_of_stock += 1

                if device:
                    linked_devices += 1

                inventory_list.append({
                    "InventoryId": inv.InventoryId,
                    "ItemCode": inv.ItemCode,
                    "ItemName": inv.ItemName,
                    "Category": inv.Category,
                    "Description": inv.Description,

                    "Device": {
                        "DeviceId": device.DeviceId,
                        "DeviceName": device.DeviceName,
                        "LastReading": device.LastReading,
                        "Weight": device.Weight,
                        "LocationName": device.LocationName,
                    } if device else None,

                    "UnitWeight": inv.UnitWeight,
                    "Stock": stock,
                    "Threshold": inv.Threshold,
                    "StockOut": inv.StockOut,
                    "Consumption": inv.Consumption,
                    "Status": status,
                    "CreatedAt": inv.CreatedAt,
                    "UpdatedAt": inv.UpdatedAt
                })

            return {
                "success": True,
                "message": "Inventory fetched successfully",
                "data": {
                    "TotalItems": total_items,
                    "LowStock": low_stock,
                    "OutOfStock": out_of_stock,
                    "LinkedDevices": linked_devices,
                    "InventoryData": inventory_list
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching inventory: {e}",
                "data": None
            }

        finally:
            await self.db_manager.disconnect()


    async def update_inventory(self, inventory_id: int, data: InventoryUpdate) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.update(
                Inventory,
                {"InventoryId": inventory_id},
                data.dict(exclude_unset=True)
            )

            if rowcount:
                return {
                    "success": True,
                    "message": "Inventory updated successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Inventory not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_inventory(self, inventory_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Inventory, {"InventoryId": inventory_id})

            if rowcount:
                return {
                    "success": True,
                    "message": "Inventory deleted successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Inventory not found"}
        finally:
            await self.db_manager.disconnect()

    # ------------------------
    # BUSINESS OPERATIONS
    # ------------------------

    async def update_stock(self, inventory_id: int, data: StockUpdate) -> dict:
        return await self.update_inventory(inventory_id, StockUpdate(**data.dict()))

    async def assign_device(self, inventory_id: int, data: DeviceAssign) -> dict:
        return await self.update_inventory(inventory_id, DeviceAssign(DeviceId=data.DeviceId))

    async def get_by_device(self, device_id: int) -> dict:
        try:
            await self.db_manager.connect()
            items = await self.db_manager.read(Inventory, {"DeviceId": device_id})

            return {
                "success": True,
                "message": "Inventory fetched by device",
                "data": [InventoryRead.from_orm(i).dict() for i in items]
            }
        finally:
            await self.db_manager.disconnect()
