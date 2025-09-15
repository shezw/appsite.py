from enum import IntEnum, StrEnum

class DBFieldType(StrEnum):
    DBField_Null = "db_null"
    DBField_Boolean = "db_boolean"   # tinyint 1
    DBField_Int = "db_int"  # tinyint 1-3     mediumint 3-6   bigint 8-13
    DBField_Float = "db_float"  # 0
    DBField_Double = "db_double"  # 0
    DBField_Decimal = "db_decimal"  # ?,?
    DBField_TimeStamp = "db_timestamp"  # bigint 13
    DBField_Location = "db_location"  # GEOMETRY ( DOUBLE )
    DBField_String = "db_string"  # varchar <=2048 ,  text >2048
    DBField_RichText = "db_richtext"  # text 65535  mediumint 16777215
    DBField_Json = "db_json"  # text 0
    DBField_ASJson = "db_asjson"  # text 0

    @staticmethod
    def get_database_clear_type(field_type: str, field_len: int) -> str:
        if field_type == DBFieldType.DBField_Null:
            return "NULL"
        elif field_type == DBFieldType.DBField_Boolean:
            return "TINYINT(1)"
        elif field_type == DBFieldType.DBField_Int:
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
        elif field_type == DBFieldType.DBField_Float:
            return "FLOAT"
        elif field_type == DBFieldType.DBField_Double:
            return "DOUBLE"
        elif field_type == DBFieldType.DBField_Decimal:
            int_len = field_len // 1000
            decimal_len = field_len % 1000
            if int_len <= 0:
                int_len = 10
            if decimal_len < 0:
                decimal_len = 2
            return f"DECIMAL({int_len},{decimal_len})"
        elif field_type == DBFieldType.DBField_TimeStamp:
            return "BIGINT(13)"
        elif field_type == DBFieldType.DBField_Location:
            return "GEOMETRY"
        elif field_type == DBFieldType.DBField_String:
            if field_len <= 0:
                field_len = 255
            if field_len > 2048:
                return "TEXT"
            else:
                return f"VARCHAR({field_len})"
        elif field_type == DBFieldType.DBField_RichText:
            if field_len <= 0:
                field_len = 65535
            if field_len > 65535:
                return "MEDIUMTEXT"
            else:
                return "TEXT"
        elif field_type == DBFieldType.DBField_Json:
            return "TEXT"
        elif field_type == DBFieldType.DBField_ASJson:
            return "TEXT"


class DBFieldIndex(StrEnum):
    DBIndex_None = 'NONE'
    DBIndex_Primary = 'PRIMARY'   # 主键索引
    DBIndex_Index = 'INDEX'       # 一般索引
    DBIndex_Unique = 'UNIQUE'     # 唯一索引
    DBIndex_FullText ='FULLTEXT'  # 分词索引
    DBIndex_Spatial = 'SPATIAL'   # 空间索引


class AsDBFieldDef:

    def __init__(self):
        self.name = ""
        self.type = DBFieldType.DBField_Null

        self.len = 0
        # !important:
        # if type is decimal, len is int len * 1000 + decimal len
        # 如果是decimal类型，len是整数长度*1000 + 小数长度

        self.nullable = False
        self.comment = ""
        self.index = DBFieldIndex.DBIndex_None

    @staticmethod
    def create(name: str, comment: str, field_type: str = DBFieldType.DBField_Null,
               field_len: int = 0, nullable: int = 1, index_type: str = DBFieldIndex.DBIndex_None) -> 'AsDBFieldDef':
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
        AsDBFieldDef.create('status', "状态 enabled 可以 ", DBFieldType.DBField_String, 12, False, DBFieldIndex.DBIndex_Index),
        AsDBFieldDef.create('createtime', '创建时间', DBFieldType.DBField_TimeStamp, 13, False, DBFieldIndex.DBIndex_Index),
        AsDBFieldDef.create('lasttime', '上一次更新时间', DBFieldType.DBField_TimeStamp, 13, False, DBFieldIndex.DBIndex_Index),
    ]


def saas_db_field() -> AsDBFieldDef:
    return AsDBFieldDef.create('saasid', '所属saas', DBFieldType.DBField_String, 8, True, DBFieldIndex.DBIndex_Index)


class AsDB:
    def __init__(self):
        pass