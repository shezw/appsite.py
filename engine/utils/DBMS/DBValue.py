from engine.core.DB import DBType, DBFieldType
import json

class DBLocationValue:
    def __init__(self, lat:float, lng:float):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return f'{{"latitude":{self.lat},"longitude":{self.lng}}}'

    def to_db(self) -> dict:
        return {
            "lat":self.lat,
            "lng":self.lng
        }


class DBValue:
    def __init__(self, field:str, f_type: DBFieldType, value):
        self.field = field
        self.value = value
        self.type = f_type

        if value is None:
            self.value = None
            return

         # Type conversion based on DBFieldType
        if self.type == DBFieldType.String:
            if not isinstance(value, str):
                self.value = str(value)
        elif self.type == DBFieldType.Int:
            if not isinstance(value, int):
                self.value = int(value)
        elif self.type == DBFieldType.Double:
            if not isinstance(value, float):
                self.value = float(value)
        elif self.type == DBFieldType.Float:
            if not isinstance(value, float):
                self.value = float(value)
        elif self.type == DBFieldType.Boolean:
            if not isinstance(value, bool):
                self.value = bool(value)
        elif self.type == DBFieldType.Json or self.type == DBFieldType.ASJson:
            if not isinstance(value, str):
                self.value = json.dumps(value, ensure_ascii=False)
        elif self.type == DBFieldType.TimeStamp:
            if not isinstance(value, int):
                self.value = int(value)
        elif self.type == DBFieldType.Decimal:
            if not isinstance(value, float):
                self.value = float(value)
        elif self.type == DBFieldType.Location:
            if not isinstance(value, DBLocationValue):
                if isinstance(value, dict):
                    if "lat" in value and "lng" in value:
                        self.value = DBLocationValue(float(value["lat"]), float(value["lng"]))
                    else:
                        raise ValueError("DBLocationValue required for Location type as {'lat':float,'lng':float}")
                else:
                    raise ValueError("DBLocationValue required for Location type")
        elif self.type == DBFieldType.RichText:
            if not isinstance(value, str):
                self.value = str(value)
        elif self.type == DBFieldType.Null:
            self.value = None
        else:
            raise ValueError("Unsupported DBFieldType")

    def get_key(self):
        return self.field

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def to_db(self, db_type:DBType = DBType.MySQL, db_major: int = 8) -> str:
        if self.value is None:
            return "NULL"

        if self.type == DBFieldType.String or self.type == DBFieldType.RichText:
            return f"'{str(self.value).replace('\'','\\\'')}'"
        elif self.type == DBFieldType.Int or self.type == DBFieldType.TimeStamp:
            return str(int(self.value))
        elif self.type == DBFieldType.Float or self.type == DBFieldType.Double or self.type == DBFieldType.Decimal:
            return str(float(self.value))
        elif self.type == DBFieldType.Boolean:
            return '1' if self.value else '0'
        elif self.type == DBFieldType.Json or self.type == DBFieldType.ASJson:
            # already converted to string at init
            return f"'{str(self.value).replace('\'','\\\'')}'"
        elif self.type == DBFieldType.Location:
            if (db_type == DBType.MySQL and db_major >= 8) or (db_type == DBType.MariaDB and db_major >= 10):
                return f"ST_GeomFromText('POINT({self.value.lng} {self.value.lat})',4326)"
            elif db_type == DBType.MySQL: # < 8
                return f"GeomFromText('POINT({self.value.lng} {self.value.lat})')"
            elif db_type == DBType.PostgreSQL:
                return f"ST_SetSRID(ST_MakePoint({self.value.lng}, {self.value.lat}), 4326)"
            elif db_type == DBType.MariaDB: # < 10
                return f"PointFromText('POINT({self.value.lng} {self.value.lat})',4326)"
            else:
                raise ValueError("Unsupported DBType for Location")
        else:
            raise ValueError("Unsupported DBFieldType")