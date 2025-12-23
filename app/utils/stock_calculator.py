from ..db.base.database_manager import DatabaseManager
from ..models.inventory_model import Inventory
from ..models.device_model import Device
from .logger import get_logger

logger = get_logger(__name__)


class StockCalculatorService:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def update_stock_by_device(self, device_id: int) -> None:
        """
        Recalculate inventory stock & status
        whenever device weight changes
        """
        try:
            await self.db_manager.connect()

            # Get device
            devices = await self.db_manager.read(Device, {"DeviceId": device_id})
            if not devices:
                logger.warning(f"Device {device_id} not found")
                return

            device = devices[0]

            # Get inventory linked to this device
            inventories = await self.db_manager.read(
                Inventory,
                {"DeviceId": device_id}
            )

            if not inventories:
                logger.info(f"No inventory linked with device {device_id}")
                return

            for inv in inventories:
                if not inv.UnitWeight or device.Weight is None:
                    continue

                # ------------------------
                # STOCK CALCULATION
                # ------------------------
                stock = int(device.Weight / inv.UnitWeight)

                # ------------------------
                # STATUS LOGIC
                # ------------------------
                if stock <= 0:
                    status = "OutOfStock"
                elif stock < inv.Threshold:
                    status = "LowStock"
                else:
                    status = "InStock"

                # ------------------------
                # UPDATE INVENTORY
                # ------------------------
                await self.db_manager.update(
                    Inventory,
                    {"InventoryId": inv.InventoryId},
                    {
                        "Stock": stock,
                        "Status": status
                    }
                )

                logger.info(
                    f"Inventory {inv.InventoryId} updated | "
                    f"Stock={stock}, Status={status}"
                )

        except Exception as e:
            logger.error(f"Stock calculation error for device {device_id}: {e}")

        finally:
            await self.db_manager.disconnect()
