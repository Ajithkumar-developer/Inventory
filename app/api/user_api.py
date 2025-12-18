from fastapi import APIRouter, HTTPException
from ..config import settings
from ..crud.user_manager import UserManager
from ..schemas.user_schema import (
    UserCreate,
    UserUpdate,
    LoginRequest
)


class UserAPI:
    def __init__(self):
        self.router = APIRouter()
        self.crud = UserManager(settings.db_type)
        self.register_routes()

    def register_routes(self):
        # Auth
        self.router.post("/auth/login")(self.login)
        self.router.post("/auth/logout")(self.logout)

        # User
        self.router.post("/users")(self.create_user)
        self.router.get("/users")(self.get_all_users)
        self.router.get("/users/{user_id}")(self.get_user)
        self.router.put("/users/{user_id}")(self.update_user)
        self.router.delete("/users/{user_id}")(self.delete_user)

    # -------- AUTH --------

    async def login(self, data: LoginRequest):
        return await self.crud.login(data)

    async def logout(self):
        return await self.crud.logout()

    # -------- USER --------

    async def create_user(self, user: UserCreate):
        return await self.crud.create_user(user)

    async def get_user(self, user_id: int):
        return await self.crud.get_user(user_id)

    async def get_all_users(self):
        return await self.crud.get_all_users()

    async def update_user(self, user_id: int, user: UserUpdate):
        return await self.crud.update_user(user_id, user)

    async def delete_user(self, user_id: int):
        return await self.crud.delete_user(user_id)
