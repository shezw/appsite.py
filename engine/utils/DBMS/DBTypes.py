from flask_babel import gettext as _
from enum import IntEnum, StrEnum

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
        AsDBFieldDef.create("sort", _('Sort Order'), DBFieldType.Int, 8, False, DBFieldIndex.Index),
        AsDBFieldDef.create("featured", _('Is featured'), DBFieldType.Boolean, 2, False, DBFieldIndex.Index),
        AsDBFieldDef.create('status', _("Status of db row"), DBFieldType.String, 12, False, DBFieldIndex.Index),
        AsDBFieldDef.create('createtime', _('Create time'), DBFieldType.TimeStamp, 13, False, DBFieldIndex.Index),
        AsDBFieldDef.create('lasttime', _('Last update time'), DBFieldType.TimeStamp, 13, False, DBFieldIndex.Index),
    ]


def saas_db_field() -> AsDBFieldDef:
    return AsDBFieldDef.create('saasid', _("Saas ID"), DBFieldType.String, 8, True, DBFieldIndex.Index)
