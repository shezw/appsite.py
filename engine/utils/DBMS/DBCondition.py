from enum import Enum

from conda.deprecations import deprecated


class DBConditionMode(Enum):
    AND = 'AND'
    OR = 'OR'
    WHERE = 'WHERE'

class DBConditionOperator(Enum):
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='
    IN = 'IN'
    BETWEEN = 'BETWEEN'
    IS_NULL = 'IS'
    NOT_NULL = 'IS NOT'
    SEARCH = 'KEYWORD'
    SEARCH_IN = 'KEYWORDS'
    MATCH = 'MATCH'


class DBCondition:
    def __init__(self, field:str, mode:DBConditionMode = DBConditionMode.AND, table:str = None):
        self.field = field
        self.mode = mode
        self.operator = DBConditionOperator.EQUAL
        self.value = None
        self.table = table

    @staticmethod
    def new( field:str, mode:DBConditionMode = DBConditionMode.AND, table:str = None):
        return DBCondition(field, mode, table)

    def get_key(self):
        return ((self.table+"." ) if self.table else "") + self.field

    def get_mode(self):
        return self.mode

    def set_mode(self, mode:DBConditionMode):
        self.mode = mode
        return self

    def search(self, keyword:str):
        self.operator = DBConditionOperator.SEARCH
        self.value = keyword
        return self

    def search_in(self, keywords:[str]):
        self.operator = DBConditionOperator.SEARCH_IN
        self.value = keywords
        return self

    def match(self, keyword:str):
        self.operator = DBConditionOperator.MATCH
        self.value = keyword
        return self

    def equal(self, value):
        self.operator = DBConditionOperator.EQUAL
        self.value = value
        return self

    def not_equal(self, value):
        self.operator = DBConditionOperator.NOT_EQUAL
        self.value = value
        return self

    def greater_than(self, value):
        self.operator = DBConditionOperator.GREATER_THAN
        self.value = value
        return self

    def less_than(self, value):
        self.operator = DBConditionOperator.LESS_THAN
        self.value = value
        return self

    def greater_equal(self, value):
        self.operator = DBConditionOperator.GREATER_EQUAL
        self.value = value
        return self

    def less_equal(self, value):
        self.operator = DBConditionOperator.LESS_EQUAL
        self.value = value
        return self

    def belong_to(self, values:[]):
        self.operator = DBConditionOperator.IN
        self.value = values
        return self

    def between(self, start, end):
        self.operator = DBConditionOperator.BETWEEN
        self.value = (start, end)
        return self

    def is_null(self):
        self.operator = DBConditionOperator.IS_NULL
        self.value = None
        return self

    def not_null(self):
        self.operator = DBConditionOperator.NOT_NULL
        self.value = None
        return self

    def boolean(self, value:bool):
        self.operator = DBConditionOperator.EQUAL
        self.value = 1 if value else 0
        return self

    def _operator_for_query(self):
        return self.operator.value

    def _value_for_query(self):
        if self.operator == DBConditionOperator.IS_NULL or self.operator == DBConditionOperator.NOT_NULL:
            return "NULL"

        if self.operator == DBConditionOperator.BETWEEN:
            if isinstance(self.value, (list, tuple)) and len(self.value) == 2:
                start = self.value[0]
                end = self.value[1]
                if isinstance(start, str):
                    start = f"'{start.replace('\'','\\\'')}'"
                if isinstance(end, str):
                    end = f"'{end.replace('\'','\\\'')}'"
                return f"{start} AND {end}"
            else:
                raise ValueError("BETWEEN operator requires a tuple or list of two values")

        if self.operator == DBConditionOperator.IN:
            if isinstance(self.value, (list, tuple)):
                formatted_values = []
                for val in self.value:
                    if isinstance(val, str):
                        formatted_values.append(f"'{val.replace('\'','\\\'')}'")
                    else:
                        formatted_values.append(str(val))
                return f"({', '.join(formatted_values)})"
            else:
                raise ValueError("IN operator requires a list or tuple of values")

        if isinstance(self.value, str):
            return f"'{self.value.replace('\'','\\\'')}'"

        return str(self.value)

    def to_query(self):
        if self.field is None or self.operator is None:
            return ""

        if self.operator is DBConditionOperator.SEARCH:
            return f"{self.mode.value} MATCH (`{self.get_key()}`) AGAINST ({self._value_for_query()} IN NATURAL LANGUAGE MODE)"

        if self.operator is DBConditionOperator.SEARCH_IN:

            search_list = self.value
            search_query = "("
            is_first = True

            if not isinstance(search_list, (list, tuple)):
                search_list = [search_list]

            for kws in search_list:
                if not isinstance(kws, str):
                    raise ValueError("SEARCH_IN operator requires a list of strings")

                if not is_first:
                    search_query += " OR "

                search_query += f"MATCH (`{self.get_key()}`) AGAINST ('{kws.replace('\'','\\\'')}' IN NATURAL LANGUAGE MODE)"

                if is_first:
                    is_first = False

            search_query += ")"
            return f"{self.mode.value} {search_query}"

        return f"{self.mode.value} `{self.get_key()}` {self._operator_for_query()} {self._value_for_query()}"
