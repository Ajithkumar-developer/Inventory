import sqlite3
from sqlite3 import Connection

class TableCreator:
    def __init__(self, sqlite_url: str):
        # Parse file path from SQLAlchemy-style URL
        if sqlite_url.startswith("sqlite+aiosqlite:///"):
            self.db_file = sqlite_url.replace("sqlite+aiosqlite:///", "")
        else:
            raise ValueError("Invalid SQLite URL format")

    def get_connection(self) -> Connection:
        return sqlite3.connect(self.db_file)



    def create_user_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT NOT NULL UNIQUE,
            PasswordHash TEXT NOT NULL,
            MobileNo TEXT,
            CreatedAt DATETIME,
            UpdatedAt DATETIME
        );
        """
        self._execute(sql, "User")


    def create_device_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Device (
            DeviceId INTEGER PRIMARY KEY AUTOINCREMENT,
            DeviceName TEXT,
            DeviceType TEXT,
            ConnectionMode TEXT,
            Capacity REAL,
            Battery INTEGER,
            Status TEXT,
            Notes TEXT,
            LocationName TEXT,
            Latitude REAL,
            Longitude REAL,
            CreatedAt DATETIME,
            UpdatedAt DATETIME
        );
        """
        self._execute(sql, "Device")

    def create_order_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orders (
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemCode TEXT,
            ItemName TEXT,
            Vendor TEXT,
            Quantity INTEGER,
            Status TEXT
        );
        """
        self._execute(sql, "Orders")
    
    # --------------------------------------------------
    # ITEM TABLE
    # --------------------------------------------------
    def create_item_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemName TEXT NOT NULL,
            Category TEXT,
            Description TEXT,
            PerUnitWeight REAL NOT NULL,
            Measurement TEXT,
            MinThreshold REAL,
            MaxThreshold REAL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "Item")

    # --------------------------------------------------
    # INVENTORY TABLE
    # --------------------------------------------------
    def create_inventory_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Inventory (
            InventoryId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER NOT NULL,
            DeviceId INTEGER,
            Weight REAL,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute(sql, "Inventory")



    # def create_inventory_table(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS Inventory (
    #         InventoryId INTEGER PRIMARY KEY AUTOINCREMENT,
    #         ItemCode TEXT,
    #         ItemName TEXT,
    #         Category TEXT,
    #         Description TEXT,
    #         DeviceId INTEGER,
    #         UnitWeight REAL,
    #         Stock REAL,
    #         Threshold REAL,
    #         StockOut REAL,
    #         Consumption REAL,
    #         Status TEXT,
    #         CreatedAt DATETIME,
    #         UpdatedAt DATETIME
    #     );
    #     """
    #     self._execute(sql, "Inventory")

    # --------------------------------------------------
    # WEIGHT TRACKING TABLE
    # --------------------------------------------------
    def create_weight_tracking_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS WeightTracking (
            WeightTrackingId INTEGER PRIMARY KEY AUTOINCREMENT,
            DeviceId INTEGER NOT NULL,
            DateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            Weight REAL NOT NULL
        );
        """
        self._execute(sql, "WeightTracking")

    # --------------------------------------------------
    # ACTIVITY LOG TABLE
    # --------------------------------------------------
    def create_activity_log_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ActivityLog (
            ActivityLogId INTEGER PRIMARY KEY AUTOINCREMENT,
            DeviceId INTEGER NOT NULL,
            DateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            Event TEXT NOT NULL
        );
        """
        self._execute(sql, "ActivityLog")

    # ------------------------------------------------------------------
    # INTERNAL HELPER
    # ------------------------------------------------------------------
    def _execute(self, sql: str, table_name: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print(f"✅ Table '{table_name}' created successfully!")
        except Exception as e:
            print(f"❌ Error creating table '{table_name}':", e)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # MAIN CREATION FUNCTION
    # ------------------------------------------------------------------
    def create_all_tables(self):
        self.create_user_table()
        self.create_device_table()
        self.create_order_table()
        self.create_item_table()
        self.create_inventory_table()
        self.create_weight_tracking_table()
        self.create_activity_log_table()



if __name__ == "__main__":
    sqlite_url = "sqlite+aiosqlite:///./inventory.db"
    creator = TableCreator(sqlite_url)
    creator.create_all_tables()