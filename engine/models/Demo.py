from engine.core.DB import AsDBFieldDef, DBFieldType, DBFieldIndex
from engine.utils.DBMS.DBTypes import common_db_fields, saas_db_field
from engine.core.Model import AsModel

class AsDemo(AsModel):

    def __init__(self):
        super().__init__()

    def table_name(self) -> str:
        return "db_demo"

    def table_comment(self) -> str:
        return "The demo table for testing"

    def primary_key(self) -> str:
        return "uid"

    def enable_log(self) -> bool:
        return True

    def enable_redis_cache(self) -> bool:
        return True

    def fields_insert(self) -> list[str] | None:
        return [
            'uid','saasid','username','password','email','mobile',
            'nickname','avatar','cover','description','introduce',
            'birthday','gender','groupid','areaid','status',]

    def fields_update(self) -> list[str] | None:
        return [
            'password', 'email', 'mobile',
            'nickname', 'avatar', 'cover', 'description', 'introduce',
            'birthday', 'gender', 'groupid', 'areaid', 'status',
        ]

    def fields_detail(self) -> list[str] | None:
        return [
            'uid', 'saasid', 'username', 'email', 'mobile', 'password',
            'nickname', 'avatar', 'cover', 'description', 'introduce',
            'birthday', 'gender', 'groupid', 'areaid', 'status', 'createtime', 'lasttime'
        ]

    def fields_public_detail(self) -> list[str] | None:
        return [
            'uid','username','email','mobile','saasid',
            'nickname','avatar','cover','description','introduce',
            'birthday','gender','groupid','areaid','status','createtime','lasttime'
        ]

    def fields_list(self) -> list[str] | None:
        return [
            'uid','username','email','mobile','saasid',
            'nickname','avatar','cover','description',
            'groupid','gender','areaid','status','createtime','lasttime'
        ]

    def fields_public_list(self) -> list[str] | None:
        return [
            'uid','username','saasid',
            'nickname','avatar','description',
            'groupid','gender','areaid','status','createtime','lasttime'
        ]

    def fields_overview(self) -> list[str] | None:
        return [
            'uid','username','saasid',
            'nickname','avatar','description','introduce',
            'groupid','areaid','createtime','lasttime'
        ]

    def fields_public_overview(self) -> list[str] | None:
        return [
            'uid','username','saasid',
            'nickname','avatar','description',
            'groupid','areaid','createtime','lasttime'
        ]

    def fields_search(self) -> list[str] | None:
        return [
            'username','email','mobile','nickname','description','introduce'
        ]

    def fields_filter(self) -> list[str] | None:
        return [
            'uid','username','email','mobile','saasid',
            'nickname','gender','groupid','areaid','status','createtime','lasttime'
        ]

    def fields_auto_convert(self) -> list[str] | None:
        return [
            'createtime','lasttime','birthday'
        ]

    def table_def(self) -> list[AsDBFieldDef] | None:
        return [
            saas_db_field(),
            AsDBFieldDef.create('uid', '用户ID 唯一索引', DBFieldType.String, 8, False,DBFieldIndex.Unique),
            AsDBFieldDef.create('groupid', '用户分组 参考user_group', DBFieldType.String, 8, False),
            AsDBFieldDef.create('areaid', '地区id', DBFieldType.String, 8, False, DBFieldIndex.Index),
            AsDBFieldDef.create('username', '用户名 账号密码登陆用', DBFieldType.String, 63, True, DBFieldIndex.Unique),
            AsDBFieldDef.create('password', '密码 hash salt加密', DBFieldType.String, 255, True),
            AsDBFieldDef.create('email', '邮箱 唯一', DBFieldType.String, 63, True, DBFieldIndex.Unique),
            AsDBFieldDef.create('mobile', '手机 唯一', DBFieldType.String, 24, True, DBFieldIndex.Unique),
            AsDBFieldDef.create('nickname', '昵称 30字以内', DBFieldType.String, 63, True),
            AsDBFieldDef.create('avatar', '头像 url', DBFieldType.String, 255, True),
            AsDBFieldDef.create('cover', '封面 url', DBFieldType.String, 255, True),
            AsDBFieldDef.create('gallery', '相册 JSON ARRAY', DBFieldType.Json, -1, True, DBFieldIndex.NONE),
            AsDBFieldDef.create('vip', '是否vip', DBFieldType.Int, 2, False, DBFieldIndex.Index),
            AsDBFieldDef.create('description', '介绍 250字以内', DBFieldType.String, 255, True),
            AsDBFieldDef.create('introduce', '简介 120字以内', DBFieldType.RichText, -1, True),
            AsDBFieldDef.create('birthday', '生日 时间戳', DBFieldType.Int, 11, True),
            AsDBFieldDef.create('gender', "性别 female male private", DBFieldType.String, 16, False),
            common_db_fields()
        ]

    def before_insert(self, data: dict) -> bool:
        # todo
        return True

    def before_update(self, data: dict) -> bool:
        # todo
        return True