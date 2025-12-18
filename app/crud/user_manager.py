from ..utils.logger import get_logger
from ..db.base.database_manager import DatabaseManager
from ..models.user_model import User
from ..schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserRead,
    LoginRequest
)

logger = get_logger(__name__)


class UserManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # ------------------------
    # USER CRUD
    # ------------------------

    async def create_user(self, user: UserCreate) -> dict:
        try:
            await self.db_manager.connect()

            data = user.dict()
            plain_password = data.pop("Password")

            # TODO: Replace with password hashing
            data["PasswordHash"] = plain_password

            obj = await self.db_manager.create(User, data)

            return {
                "success": True,
                "message": "User created successfully",
                "data": UserRead.from_orm(obj).dict()
            }

        except Exception as e:
            logger.error(f"Create user error: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_user(self, user_id: int) -> dict:
        try:
            await self.db_manager.connect()
            result = await self.db_manager.read(User, {"UserId": user_id})

            if result:
                return {
                    "success": True,
                    "message": "User fetched successfully",
                    "data": UserRead.from_orm(result[0]).dict()
                }

            return {"success": False, "message": "User not found", "data": None}

        finally:
            await self.db_manager.disconnect()

    async def get_all_users(self) -> dict:
        try:
            await self.db_manager.connect()
            users = await self.db_manager.read(User)

            return {
                "success": True,
                "message": "Users fetched successfully",
                "data": [UserRead.from_orm(u).dict() for u in users]
            }

        finally:
            await self.db_manager.disconnect()

    async def update_user(self, user_id: int, data: UserUpdate) -> dict:
        try:
            await self.db_manager.connect()

            update_data = data.dict(exclude_unset=True)

            if "Password" in update_data:
                update_data["PasswordHash"] = update_data.pop("Password")

            rowcount = await self.db_manager.update(
                User,
                {"UserId": user_id},
                update_data
            )

            if rowcount:
                return {
                    "success": True,
                    "message": "User updated successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "User not found"}

        finally:
            await self.db_manager.disconnect()

    async def delete_user(self, user_id: int) -> dict:
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(User, {"UserId": user_id})

            if rowcount:
                return {
                    "success": True,
                    "message": "User deleted successfully",
                    "data": {"rows_affected": rowcount}
                }

            return {"success": False, "message": "User not found"}

        finally:
            await self.db_manager.disconnect()

    # ------------------------
    # AUTH (SAME MANAGER)
    # ------------------------

    async def login(self, login: LoginRequest) -> dict:
        try:
            await self.db_manager.connect()

            result = await self.db_manager.read(User, {"Email": login.Email})
            if not result:
                return {"success": False, "message": "Invalid credentials"}

            user = result[0]

            # TODO: hash comparison
            if user.PasswordHash != login.Password:
                return {"success": False, "message": "Invalid credentials"}

            return {
                "success": True,
                "message": "Login successful",
                "data": {
                    "UserId": user.UserId,
                    "Email": user.Email
                }
            }

        finally:
            await self.db_manager.disconnect()

    async def logout(self) -> dict:
        return {
            "success": True,
            "message": "Logout successful"
        }
