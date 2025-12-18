from fastapi import APIRouter
from ..config import settings
from ..crud.order_manager import OrderManager
from ..schemas.order_schema import OrderCreate, OrderUpdate


class OrderAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = OrderManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        self.router.post("/orders")(self.create_order)
        self.router.get("/orders")(self.get_all_orders)
        self.router.get("/orders/{order_id}")(self.get_order)
        self.router.put("/orders/{order_id}")(self.update_order)
        self.router.delete("/orders/{order_id}")(self.delete_order)

    async def create_order(self, order: OrderCreate):
        return await self.crud.create_order(order)

    async def get_order(self, order_id: int):
        return await self.crud.get_order(order_id)

    async def get_all_orders(self):
        return await self.crud.get_all_orders()

    async def update_order(self, order_id: int, order: OrderUpdate):
        return await self.crud.update_order(order_id, order)

    async def delete_order(self, order_id: int):
        return await self.crud.delete_order(order_id)
