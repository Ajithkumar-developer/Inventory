from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.user_api import UserAPI
from .api.device_api import DeviceAPI
from .api.order_api import OrderAPI
from .api.inventory_api import InventoryAPI, WeightTrackingAPI, ActivityLogAPI
from .api.item_api import ItemAPI

app = FastAPI(title="User & Auth API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (DEV ONLY)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_api = UserAPI()
device_api = DeviceAPI()
order_api = OrderAPI()
inventory_api = InventoryAPI()
weight_tracking_api = WeightTrackingAPI()
activity_log_api = ActivityLogAPI()
item_api = ItemAPI()


app.include_router(user_api.router, tags=["User"])
app.include_router(device_api.router, tags=["Device"])
app.include_router(order_api.router, tags=["Order"])
app.include_router(inventory_api.router, tags=["Inventory"])
app.include_router(weight_tracking_api.router, tags=["Weight Tracking"])
app.include_router(activity_log_api.router, tags=["Activity Log"])
app.include_router(item_api.router, tags=["Item"])