from abc import abstractmethod
from flask_babel import gettext as _
from engine.utils.DBMS.DBTypes import DBType, DBFieldType, DBFieldIndex, AsDBFieldDef
from engine.utils.DBMS.DBValues import DBValues
from engine.utils.DBMS.DBConditions import DBConditions

asdb_mysql_singleton = None
asdb_postgresql_singleton = None
asdb_mariadb_singleton = None

class AsDB:
    def __init__(self, db_type: DBType = DBType.Unknown):
        self.host = ""
        self.port = 0
        self.user = ""
        self.password = ""
        self.database = ""
        self.db_type = db_type
        self.charset = "utf8mb4"
        self.table_prefix = ""
        self.is_connected = False
        self.connection = None

    def __del__(self):
        self.close()

    @staticmethod
    def shared( db_type: DBType, host: str = None, port: int = None, user: str = None, password: str = None, database: str = None, table_prefix: str = "", charset: str = "utf8mb4" ):

        global asdb_mysql_singleton
        global asdb_postgresql_singleton
        global asdb_mariadb_singleton

        if db_type == DBType.MySQL:
            if asdb_mysql_singleton is not None and asdb_mysql_singleton.is_connected:
                return asdb_mysql_singleton
        elif db_type == DBType.PostgreSQL:
            if asdb_postgresql_singleton is not None and asdb_postgresql_singleton.is_connected:
                return asdb_postgresql_singleton
        elif db_type == DBType.MariaDB:
            if asdb_mariadb_singleton is not None and asdb_mariadb_singleton.is_connected:
                return asdb_mariadb_singleton

        db = AsDB(db_type)

        db.host = host
        db.port = port
        db.user = user
        db.password = password
        db.database = database
        db.charset = charset
        db.table_prefix = table_prefix

        if not db.is_connected:
            db.connect()

        if not db.is_connected:
            return None

        if db_type == DBType.MySQL:
            asdb_mysql_singleton = db
        elif db_type == DBType.PostgreSQL:
            asdb_postgresql_singleton = db
        elif db_type == DBType.MariaDB:
            asdb_mariadb_singleton = db

        return db

    @staticmethod
    def active():
        global asdb_mysql_singleton
        global asdb_postgresql_singleton
        global asdb_mariadb_singleton

        if asdb_mysql_singleton is not None and asdb_mysql_singleton.is_connected:
            return asdb_mysql_singleton
        if asdb_postgresql_singleton is not None and asdb_postgresql_singleton.is_connected:
            return asdb_postgresql_singleton
        if asdb_mariadb_singleton is not None and asdb_mariadb_singleton.is_connected:
            return asdb_mariadb_singleton

        return None

    def connect(self) -> bool:
        if self.db_type == DBType.MySQL:
            return self.connect_mysql()
        elif self.db_type == DBType.PostgreSQL:
            return self.connect_postgresql()
        else:
            return False


    @staticmethod
    def mariadb( host: str = None, port: int = None, user: str = None, password: str = None, database: str = None, table_prefix: str = "", charset: str = "utf8mb4" ):
        return AsDB.shared(DBType.MariaDB, host, port, user, password, database, table_prefix, charset)

    @staticmethod
    def mysql( host: str = None, port: int = None, user: str = None, password: str = None, database: str = None, table_prefix: str = "", charset: str = "utf8mb4" ):
        return AsDB.shared(db_type=DBType.MySQL, host=host, port=port, user=user, password=password, database=database, table_prefix=table_prefix, charset=charset)

    @staticmethod
    def postgresql( host: str = None, port: int = None, user: str = None, password: str = None, database: str = None, table_prefix: str = "", charset: str = "utf8mb4" ):
        return AsDB.shared(db_type=DBType.PostgreSQL, host=host, port=port, user=user, password=password, database=database, table_prefix=table_prefix, charset=charset)

    def connect_mysql(self):
        import pymysql
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
            )
            self.is_connected = True

        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            self.is_connected = False

        print(f"MySQL connected: {self.is_connected}")
        return self.is_connected

    def connect_postgresql(self):
        import psycopg2
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.is_connected = True

        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            self.is_connected = False

        print(f"PostgreSQL connected: {self.is_connected}")
        return self.is_connected

    def connect_mariadb(self):
        # todo
        pass

    def get_version(self):
        if not self.is_connected or self.connection is None:
            return None

        try:
            cursor = self.connection.cursor()
            if self.db_type == DBType.MySQL or self.db_type == DBType.MariaDB:
                cursor.execute("SELECT VERSION()")
            elif self.db_type == DBType.PostgreSQL:
                cursor.execute("SHOW server_version")
            version = cursor.fetchone()
            cursor.close()
            if version:
                return version[0]
            return None
        except Exception as e:
            print(f"Error getting database version: {e}")
            return None

    def get_versions(self):
        version_str = self.get_version()
        if version_str is None:
            return 0, 0, 0

        parts = version_str.split(".")
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

        return major, minor, patch

    def get_version_major(self):
        major, _, _ = self.get_versions()
        return major

    def get_version_minor(self):
        _, minor, _ = self.get_versions()
        return minor

    def get_version_patch(self):
        _, _, patch = self.get_versions()
        return patch

    def close(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
            self.connection = None

    def _insert(self, values:DBValues, table:str) -> str | None:
        if not self.is_connected or self.connection is None:
            return None

        if values is None or len(values.values) == 0:
            return None

        return f"INSERT INTO `{self.table_prefix}{table}` SET {values.to_db(self.db_type, self.get_version_major())}"


    def _update(self, values:DBValues, table:str, condition:DBConditions ) -> str | None:
        pass


    def insert(self, values:DBValues, table:str) -> bool:

        _query = self._insert(values, table)

        if _query is None:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(_query)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            return False

