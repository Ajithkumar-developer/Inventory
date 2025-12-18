from ..utils.logger import get_logger
from ..db.base.database_manager import DatabaseManager
from ..models.order_model import Order
from ..schemas.order_schema import (
    OrderCreate,
    OrderUpdate,
    OrderRead
)

logger = get_logger(__name__)


class OrderManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    async def create_order(self, order: OrderCreate) -> dict:
        try:
            await self.db_manager.connect()
            obj = await self.db_manager.create(Order, order.dict())

            return {
                "success": True,
                "message": "Order created successfully",
                "data": OrderRead.from_orm(obj).dict()
            }
        finally:
            await self.db_manager.disconnect()

    async def get_order(self, order_id: int) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(Order, {"OrderId": order_id})

            if result:
                return {
                    "success": True,
                    "message": "Order fetched successfully",
                    "data": OrderRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "Order not found", "data": None}
        finally:
            await self.db_manager.disconnect()

    async def get_all_orders(self) -> dict:
        try:
            await self.db_manager.connect()
            orders = await self.db_manager.read(Order)

            # Initialize status counters
            status_count = {
                "Delivered": 0,
                "Pending": 0,
                "Cancelled": 0,
                "InTransit": 0
            }

            order_list = []

            for o in orders:
                # Count order status safely
                if o.Status in status_count:
                    status_count[o.Status] += 1

                order_list.append(OrderRead.from_orm(o).dict())

            return {
                "success": True,
                "message": "Orders fetched successfully",
                "data": {
                    **status_count,
                    "Orders": order_list
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching orders: {e}",
                "data": None
            }
        finally:
            await self.db_manager.disconnect()


    async def update_order(self, order_id: int, data: OrderUpdate) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.update(
                Order,
                {"OrderId": order_id},
                data.dict(exclude_unset=True)
            )

            if rowcount:
                return {
                    "success": True,
                    "message": "Order updated successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Order not found"}
        finally:
            await self.db_manager.disconnect()

    async def delete_order(self, order_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Order, {"OrderId": order_id})

            if rowcount:
                return {
                    "success": True,
                    "message": "Order deleted successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "Order not found"}
        finally:
            await self.db_manager.disconnect()
