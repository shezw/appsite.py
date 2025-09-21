from engine.utils.DBMS.DBCondition import DBCondition, DBConditionMode
from engine.utils.DBMS.DBTypes import DBOrderDirection, DBType

default_page_size = 20

class DBConditions:
    def __init__(self, table:str = None ):
        global default_page_size
        self.table = table
        self.conditions: [DBCondition] = []
        self.params = []
        self.group = None
        self.page = 1
        self.page_size = default_page_size
        self.order_list = []

    @staticmethod
    def new( table:str = None ):
        return DBConditions(table)

    def __add__(self, other):
        if isinstance(other, DBCondition):
            self.conditions.append(other)
        elif isinstance(other, DBConditions):
            for cond in other.conditions:
                self.conditions.append(cond)
        return self

    def get_key(self, field:str):
        return ((self.table+"." ) if self.table else "") + field

    def add(self, condition:DBCondition):
        if isinstance(condition, DBCondition):
            self.conditions.append(condition)
        return self

    def where(self, field:str):
        cond = DBCondition.new(field, DBConditionMode.WHERE, self.table)
        self.conditions.append(cond)
        return self

    def and_where(self, field:str):
        cond = DBCondition.new(field, DBConditionMode.AND, self.table)
        self.conditions.append(cond)
        return self

    def or_where(self, field:str):
        cond = DBCondition.new(field, DBConditionMode.OR, self.table)
        self.conditions.append(cond)
        return self

    def order_by(self, field:str, direction:DBOrderDirection = DBOrderDirection.Asc):
        self.order_list.append({"field": field, "direction": direction, "type":"normal"})
        return self

    def order_by_distance(self, latitude:float, longitude:float, field:str = "location", direction:DBOrderDirection = DBOrderDirection.Asc):
        self.order_list.append({"field": field, "latitude": latitude, "longitude": longitude, "direction": direction, "type":"distance"})
        return self

    def is_ordered(self):
        return len(self.order_list) > 0

    def limit_with(self, page:int, page_size:int):
        if page > 0:
            self.page = page
        if page_size > 0:
            self.page_size = page_size
        return self

    def group_by(self, field:str):
        self.group = field
        return self

    def search(self, keyword:str):
        self.conditions[-1].search(keyword)
        return self

    def search_in(self, keywords:[str]):
        self.conditions[-1].search_in(keywords)
        return self

    def match(self, keyword:str):
        self.conditions[-1].match(keyword)
        return self

    def belong_to(self, values:list):
        self.conditions[-1].belong_to(values)
        return self

    def between(self, start, end):
        self.conditions[-1].between(start, end)
        return self

    def equal(self, value):
        self.conditions[-1].equal(value)
        return self

    def not_equal(self, value):
        self.conditions[-1].not_equal(value)
        return self

    def greater_than(self, value):
        self.conditions[-1].greater_than(value)
        return self

    def less_than(self, value):
        self.conditions[-1].less_than(value)
        return self

    def greater_equal(self, value):
        self.conditions[-1].greater_equal(value)
        return self

    def less_equal(self, value):
        self.conditions[-1].less_equal(value)
        return self

    def is_empty(self):
        return len(self.conditions) == 0

    def is_null(self):
        self.conditions[-1].is_null()
        return self

    def not_null(self):
        self.conditions[-1].not_null()
        return self

    def is_true(self):
        self.conditions[-1].boolean(True)
        return self

    def is_false(self):
        self.conditions[-1].boolean(False)
        return self

    def is_bool(self, value:bool):
        self.conditions[-1].boolean(value)
        return self


    def purify(self, filters:list):
        for cond in self.conditions:
            if cond.field not in filters:
                self.conditions.remove(cond)
        return self

    def condition_to_query(self, use_and:bool = False):
        query = ""
        if len(self.conditions) == 0:
            return query

        if use_and:
            self.conditions[0].set_mode(DBConditionMode.AND)

        for cond in self.conditions:
            query += f" {cond.to_query()}"

        return query.strip()

    def order_to_query(self):
        from engine.core.DB import AsDB
        db = AsDB.active()
        query = ""
        if len(self.order_list) == 0:
            return query

        order_clauses = []
        for order in self.order_list:
            if order["type"] == "normal":
                order_clauses.append(f"`{self.get_key(order['field'])}` {order['direction'].value}")
            elif order["type"] == "distance":

                if db is not None and db.db_type == DBType.MySQL:
                    db_ver = db.get_version_major()
                    if db_ver >= 8:
                        order_clauses.append(f"GLength(LineStringFromWKB(LineString(`{self.get_key(order['field'])}`, POINT({order['longitude']} {order['latitude']})))) {order['direction'].value}")
                    else:
                        order_clauses.append(f"GLength(ST_LineStringFromWKB(LineString(`{self.get_key(order['field'])}`, POINT({order['longitude']} {order['latitude']})))) {order['direction'].value}")

        if len(order_clauses) > 0:
            query = " ORDER BY " + ", ".join(order_clauses)

        return query

    def group_to_query(self):
        query = ""
        if self.group is None or self.group == "":
            return query
        query = f" GROUP BY `{self.get_key(self.group)}`"
        return query

    def limit_to_query(self):
        from engine.core.DB import AsDB
        query = ""
        if self.page_size <= 0:
            return query
        offset = (self.page - 1) * self.page_size

        db = AsDB.active()

        if db.db_type == DBType.PostgreSQL:
            query = f" LIMIT {self.page_size} OFFSET {offset}"
            return query

        # Default is MySQL/MariaDB
        query = f" LIMIT {offset},{self.page_size}"
        return query

    def to_query(self, use_and:bool = False):
        query = self.condition_to_query(use_and)
        query += self.group_to_query()
        query += self.order_to_query()
        query += self.limit_to_query()
        return query.strip()