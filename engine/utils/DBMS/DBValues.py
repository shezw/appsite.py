from engine.core.DB import DBType, DBFieldType
from engine.utils.DBMS.DBValue import DBValue


class DBValues:
    def __init__(self):
        self.values:dict = {}
        self.indexes = []

    @staticmethod
    def new( field:str = None):
        vals = DBValues()
        if field is None:
            return vals

        return vals.add(field)

    def add(self, field:str ):
        if field not in self.indexes:
            self.indexes.append(field)
            self.values[field] = None
        return self

    def set(self, field:str):
        return self.add(field)

    def to(self, f_type:DBFieldType, value):
        if len(self.indexes) == 0:
            return self

        field = self.indexes[-1]
        self.values[field] = DBValue(field, f_type, value)
        return self

    def to_int(self, value):
        return self.to(DBFieldType.Int, value)

    def to_double(self, value):
        return self.to(DBFieldType.Double, value)

    def to_float(self, value):
        return self.to(DBFieldType.Float, value)

    def to_boolean(self, value):
        return self.to(DBFieldType.Boolean, value)

    def to_json(self, value):
        return self.to(DBFieldType.Json, value)

    def to_asjson(self, value):
        return self.to(DBFieldType.ASJson, value)

    def to_timestamp(self, value):
        return self.to(DBFieldType.TimeStamp, value)

    def to_decimal(self, value):
        return self.to(DBFieldType.Decimal, value)

    def to_location(self, value):
        return self.to(DBFieldType.Location, value)

    def to_null(self):
        return self.to(DBFieldType.Null, None)

    def to_string(self, value):
        return self.to(DBFieldType.String, value)

    def to_richtext(self, value):
        return self.to(DBFieldType.RichText, value)

    def get_keys(self):
        return list(self.values.keys())

    def is_key_exists(self, key:str):
        return key in self.values

    def get_value_of(self, key:str):
        if key in self.values:
            return self.values[key]
        return None

    def purify(self, filters:list):

        for key in self.indexes:
            if key not in filters:
                self.values.pop(key, None)
                self.indexes.remove(key)
        return self

    def to_dict(self):
        return self.values

    def to_list(self):
        return [{key:self.values[key]} for key in self.indexes]

    def to_db(self, db_type:DBType = DBType.MySQL, db_major: int = 8) -> str:
        items = []
        for key in self.indexes:
            value = self.values[key]
            if value is None:
                continue
            if not isinstance(value, DBValue):
                continue
            db_value = value.to_db(db_type, db_major)
            items.append(f"`{key}`={db_value}")
        return ", ".join(items)