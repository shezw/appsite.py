from abc import abstractmethod
from enum import IntEnum, StrEnum
from flask_babel import gettext as _

class DBType(StrEnum):
    Unknown = "unknown"
    MySQL = "mysql"
    PostgreSQL = "postgresql"
    MariaDB = "mariadb"

class DBFieldType(StrEnum):
    Null = "db_null"
    Boolean = "db_boolean"   # tinyint 1
    Int = "db_int"  # tinyint 1-3     mediumint 3-6   bigint 8-13
    Float = "db_float"  # 0
    Double = "db_double"  # 0
    Decimal = "db_decimal"  # ?,?
    TimeStamp = "db_timestamp"  # bigint 13
    Location = "db_location"  # GEOMETRY ( DOUBLE )
    String = "db_string"  # varchar <=2048 ,  text >2048
    RichText = "db_richtext"  # text 65535  mediumint 16777215
    Json = "db_json"  # text 0
    ASJson = "db_asjson"  # text 0

    @staticmethod
    def get_database_clear_type(field_type: str, field_len: int) -> str:
        if field_type == DBFieldType.Null:
            return "NULL"
        elif field_type == DBFieldType.Boolean:
            return "TINYINT(1)"
        elif field_type == DBFieldType.Int:
            if field_len <= 3:
                return "TINYINT(3)"
            elif field_len <= 6:
                return "MEDIUMINT(6)"
            elif field_len <= 8:
                return "INT(8)"
            elif field_len <= 13:
                return "BIGINT(13)"
            else:
                return "BIGINT"
        elif field_type == DBFieldType.Float:
            return "FLOAT"
        elif field_type == DBFieldType.Double:
            return "DOUBLE"
        elif field_type == DBFieldType.Decimal:
            int_len = field_len // 1000
            decimal_len = field_len % 1000
            if int_len <= 0:
                int_len = 10
            if decimal_len < 0:
                decimal_len = 2
            return f"DECIMAL({int_len},{decimal_len})"
        elif field_type == DBFieldType.TimeStamp:
            return "BIGINT(13)"
        elif field_type == DBFieldType.Location:
            return "GEOMETRY"
        elif field_type == DBFieldType.String:
            if field_len <= 0:
                field_len = 255
            if field_len > 2048:
                return "TEXT"
            else:
                return f"VARCHAR({field_len})"
        elif field_type == DBFieldType.RichText:
            if field_len <= 0:
                field_len = 65535
            if field_len > 65535:
                return "MEDIUMTEXT"
            else:
                return "TEXT"
        elif field_type == DBFieldType.Json:
            return "TEXT"
        elif field_type == DBFieldType.ASJson:
            return "TEXT"


class DBFieldIndex(StrEnum):
    NONE = 'NONE'
    Primary = 'PRIMARY'   # 主键索引
    Index = 'INDEX'       # 一般索引
    Unique = 'UNIQUE'     # 唯一索引
    FullText ='FULLTEXT'  # 分词索引
    Spatial = 'SPATIAL'   # 空间索引


class AsDBFieldDef:

    def __init__(self):
        self.name = ""
        self.type = DBFieldType.Null

        self.len = 0
        # !important:
        # if type is decimal, len is int len * 1000 + decimal len
        # 如果是decimal类型，len是整数长度*1000 + 小数长度

        self.nullable = False
        self.comment = ""
        self.index = DBFieldIndex.NONE

    @staticmethod
    def create(name: str, comment: str, field_type: str = DBFieldType.Null,
               field_len: int = 0, nullable: int = 1, index_type: str = DBFieldIndex.NONE) -> 'AsDBFieldDef':
        field = AsDBFieldDef()
        field.name = name
        field.type = field_type
        field.len = field_len
        field.nullable = (nullable != 0)
        field.comment = comment
        field.index = index_type
        return field


def common_db_fields() -> list[AsDBFieldDef]:
    return [
        AsDBFieldDef.create("sort", _('Sort Order'), DBFieldType.Int, 0, DBFieldIndex.INDEXED, False, "Sort Order"),
        AsDBFieldDef.create("featured", _('Is featured'), DBFieldType.Boolean, 0, DBFieldIndex.INDEXED, False, "Is Featured"),
        AsDBFieldDef.create('status', _("Status of db row"), DBFieldType.String, 12, False, DBFieldIndex.Index),
        AsDBFieldDef.create('createtime', _('Create time'), DBFieldType.TimeStamp, 13, False, DBFieldIndex.Index),
        AsDBFieldDef.create('lasttime', _('Last update time'), DBFieldType.TimeStamp, 13, False, DBFieldIndex.Index),
    ]


def saas_db_field() -> AsDBFieldDef:
    return AsDBFieldDef.create('saasid', '所属saas', DBFieldType.String, 8, True, DBFieldIndex.Index)

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

    def connect(self) -> bool:
        if self.db_type == DBType.MySQL:
            return self.connect_mysql()
        elif self.db_type == DBType.PostgreSQL:
            return self.connect_postgresql()
        else:
            return False


    @staticmethod
    def mariadb(host: str, port: int, user: str, password: str, database: str, table_prefix: str = "", charset: str = "utf8mb4"):
        return AsDB.shared(DBType.MariaDB, host, port, user, password, database, table_prefix, charset)

    @staticmethod
    def mysql(host: str, port: int, user: str, password: str, database: str, table_prefix: str = "", charset: str = "utf8mb4"):
        return AsDB.shared(db_type=DBType.MySQL, host=host, port=port, user=user, password=password, database=database, table_prefix=table_prefix, charset=charset)

    @staticmethod
    def postgresql(host: str, port: int, user: str, password: str, database: str, table_prefix: str = "", charset: str = "utf8mb4"):
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