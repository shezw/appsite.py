import unittest
import includes
from engine.core.DB import DBType, AsDB
from engine.utils.DBMS.DBConditions import DBConditions
from engine.utils.DBMS.DBCondition import DBCondition, DBConditionMode

test_demo_db = "appsite_py"
test_demo_prefix = "aps_"
test_demo_user = "appsite_py"
test_demo_password = "JAN87123nz"

class MyTestCase(unittest.TestCase):
    def test_01_mysql(self):

        db = AsDB.mysql(
            host="localhost",
            port=3306,
            user=test_demo_user,
            password=test_demo_password,
            database=test_demo_db,
            table_prefix=test_demo_prefix,
            charset="utf8mb4"
        )

        self.assertIsNotNone(db)

        self.assertEqual(db.host, "localhost")
        self.assertEqual(db.port, 3306)
        self.assertEqual(db.user, test_demo_user)
        self.assertEqual(db.password, test_demo_password)
        self.assertEqual(db.database, test_demo_db)
        self.assertEqual(db.table_prefix, test_demo_prefix)
        self.assertEqual(db.charset, "utf8mb4")
        self.assertEqual(db.db_type, DBType.MySQL)

        connected = db.connect()
        self.assertTrue(connected)
        self.assertTrue(db.is_connected)

        print("MySQL Server Version:", db.get_version())

    def test_02_db_values(self):

        db_values = {
            'string': 'test_string',
            'int': 123,
            'float': 123.456,
            'bool_true': True,
            'bool_false': False,
            'none': None,
        }
        from engine.core.DB import DBFieldType
        from engine.utils.DBMS.DBValues import DBValues
        vals = DBValues.new() \
            .set('string').to_string(db_values['string']) \
            .set('int').to_int(db_values['int']) \
            .set('float').to_float(db_values['float']) \
            .set('bool_true').to_boolean(db_values['bool_true']) \
            .set('bool_false').to_boolean(db_values['bool_false']) \
            .set('none').to_string(db_values['none']) \
            .set("json").to_json({"key":"value"}) \
            .set("location").to_location({"lat":12.34,"lng":56.78}) \
            .set("timestamp").to_timestamp(1625077765) \
            .set("decimal").to_decimal(12345.6789) \
            .set("double").to_double(123.456789) \
            .set("asjson").to_asjson({"a":1,"b":2}) \
            .set("richtext").to_richtext( "<p style='font-size:128px'>This is rich text</p>")

        self.assertEqual(len(vals.values), 13)
        self.assertEqual(vals.values['string'].value, db_values['string'])
        self.assertEqual(vals.values['int'].value, db_values['int'])
        self.assertEqual(vals.values['float'].value, db_values['float'])
        self.assertEqual(vals.values['bool_true'].value, db_values['bool_true'])
        self.assertEqual(vals.values['bool_false'].value, db_values['bool_false'])
        self.assertIsNone(vals.values['none'].value)
        self.assertEqual(vals.values['json'].value, '{"key": "value"}')
        self.assertEqual(vals.values['location'].value.lat, 12.34)
        self.assertEqual(vals.values['location'].value.lng, 56.78)
        self.assertEqual(vals.values['timestamp'].value, 1625077765)
        self.assertEqual(vals.values['decimal'].value, 12345.6789)
        self.assertEqual(vals.values['double'].value, 123.456789)
        self.assertEqual(vals.values['asjson'].value, '{"a": 1, "b": 2}')
        self.assertEqual(vals.values['richtext'].value, "<p style=\'font-size:128px\'>This is rich text</p>")

        print(AsDB.mysql())
        print(vals.values)
        print(AsDB.mysql()._insert(table="test_table", values=vals))
        self.assertEqual(AsDB.mysql()._insert(table="test_table", values=vals),"INSERT INTO `aps_test_table` SET `string`='test_string', `int`=123, `float`=123.456, `bool_true`=1, `bool_false`=0, `none`=NULL, `json`='{\"key\": \"value\"}', `location`=ST_GeomFromText('POINT(56.78 12.34)',4326), `timestamp`=1625077765, `decimal`=12345.6789, `double`=123.456789, `asjson`='{\"a\": 1, \"b\": 2}', `richtext`='<p style=\\\'font-size:128px\\\'>This is rich text</p>'")
        print(vals.to_db(DBType.MySQL,AsDB.mysql().get_version_major()))

    def test_03_db_condition(self):

        cond0 = DBCondition.new("name").equal("John").set_mode(DBConditionMode.WHERE)
        self.assertEqual(cond0.to_query(), "WHERE `name` = 'John'")

        cond1 = DBCondition.new("age").greater_than(18)
        self.assertEqual(cond1.to_query(), "AND `age` > 18")

        cond1_1 = DBCondition.new("age",table="user_account").greater_than(18)
        self.assertEqual(cond1_1.to_query(), "AND `user_account.age` > 18")

        cond2 = DBCondition.new("status").belong_to(["active", "pending"])
        self.assertEqual(cond2.to_query(), "AND `status` IN ('active', 'pending')")

        cond3 = DBCondition.new("createtime").between(1625077765, 1625164165)
        self.assertEqual(cond3.to_query(), "AND `createtime` BETWEEN 1625077765 AND 1625164165")

        cond4 = DBCondition.new("description").search("llm")
        self.assertEqual(cond4.to_query(), "AND MATCH (`description`) AGAINST ('llm' IN NATURAL LANGUAGE MODE)")

        cond5 = DBCondition.new("content",table="news").search_in(["llm","cnn","machine learning"])
        self.assertEqual(cond5.to_query(), "AND (MATCH (`news.content`) AGAINST ('llm' IN NATURAL LANGUAGE MODE) OR MATCH (`news.content`) AGAINST ('cnn' IN NATURAL LANGUAGE MODE) OR MATCH (`news.content`) AGAINST ('machine learning' IN NATURAL LANGUAGE MODE))")

        cond6 = DBCondition.new("weichatid").is_null()
        self.assertEqual(cond6.to_query(), "AND `weichatid` IS NULL")

if __name__ == '__main__':
    unittest.main()
