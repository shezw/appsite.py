from engine.utils.DBMS.DBCondition import DBCondition

class DBConditions:
    def __init__(self, table:str ):
        self.table = table
        self.conditions: [DBCondition] = []
        self.params = []

    @staticmethod
    def new( table:str ):
        return DBConditions(table)

