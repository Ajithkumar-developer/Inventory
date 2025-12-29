from ..db.base.database_manager import DatabaseManager
from ..models.item_model import Item
from ..schemas.item_schema import ItemCreate, ItemUpdate, ItemRead
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ItemManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_item(self, item: ItemCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(Item, item.dict())

            return {
                "success": True,
                "message": "Item created successfully",
                "data": ItemRead.from_orm(obj).dict()
            }

        except Exception as e:
            logger.error(f"Create item error: {e}")
            return {"success": False, "message": str(e), "data": None}

        finally:
            await self.db_manager.disconnect()

    async def get_item(self, item_id: int) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(Item, {"ItemId": item_id})

            if not result:
                return {"success": False, "message": "Item not found", "data": None}

            return {
                "success": True,
                "message": "Item fetched successfully",
                "data": ItemRead.from_orm(result[0]).dict()
            }

        finally:
            await self.db_manager.disconnect()

    async def get_all_items(self) -> dict:
        try:
            await self.db_manager.connect()
            items = await self.db_manager.read(Item)

            return {
                "success": True,
                "message": "Items fetched successfully",
                "data": [ItemRead.from_orm(i).dict() for i in items]
            }

        finally:
            await self.db_manager.disconnect()

    async def update_item(self, item_id: int, data: ItemUpdate) -> dict:
        try:
            await self.db_manager.connect()
            update_data = data.dict(exclude_unset=True)

            rows = await self.db_manager.update(
                Item,
                {"ItemId": item_id},
                update_data
            )

            return {
                "success": bool(rows),
                "message": "Item updated successfully" if rows else "Item not found",
                "data": {"rows_affected": rows}
            }

        finally:
            await self.db_manager.disconnect()

    async def delete_item(self, item_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rows = await self.db_manager.delete(Item, {"ItemId": item_id})

            return {
                "success": bool(rows),
                "message": "Item deleted successfully" if rows else "Item not found",
                "data": {"rows_affected": rows}
            }

        finally:
            await self.db_manager.disconnect()
