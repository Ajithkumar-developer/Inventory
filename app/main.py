from fastapi import FastAPI
from .api.user_api import UserAPI
from .api.device_api import DeviceAPI
from .api.order_api import OrderAPI
from .api.inventory_api import InventoryAPI





app = FastAPI(title="User & Auth API")

user_api = UserAPI()
device_api = DeviceAPI()
order_api = OrderAPI()
inventory_api = InventoryAPI()



app.include_router(user_api.router, tags=["User"])
app.include_router(device_api.router, tags=["Device"])
app.include_router(order_api.router, tags=["Order"])
app.include_router(inventory_api.router, tags=["Inventory"])
