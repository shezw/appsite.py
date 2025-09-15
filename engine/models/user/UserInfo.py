from engine.core.DB import AsDBFieldDef, DBFieldType, DBFieldIndex, common_db_fields, saas_db_field
from engine.core.Model import AsModel

class UserInfo(AsModel):

    def __init__(self, userid:str=None):
        super().__init__()
        self.userid = userid

    def table_name(self) -> str:
        return "user_info"

    def table_comment(self) -> str:
        return "User Info Table"

    def primary_key(self) -> str:
        return "userid"

    def enable_log(self) -> bool:
        return True

    def enable_redis_cache(self) -> bool:
        return True


    def fields_insert(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'gallery',
            'realname','idnumber',
            'country','province','city','company',
            'wechatid','weiboid','qqid','appleUUID','deviceID',
            'facebookid','twitterid','douyinid','ticktokid','googleid',
            'status','realstatus',
        ]

    def fields_update(self) -> list[str] | None:
        return [
            'vip','vipexpire',
            'gallery',
            'realname','idnumber',
            'country','province','city','company',
            'wechatid','weiboid','qqid','appleUUID','deviceID',
            'facebookid','twitterid','douyinid','ticktokid','googleid',
            'status','realstatus',
        ]

    def fields_detail(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'gallery',
            'realname','idnumber',
            'country','province','city','company',
            'wechatid','weiboid','qqid','appleUUID','deviceID',
            'facebookid','twitterid','douyinid','ticktokid','googleid',
            'status','realstatus',
        ]

    def fields_public_detail(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'gallery',
            'country','province','city','company',
            'status','realstatus',
        ]

    def fields_list(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'realname','idnumber',
            'country','province','city','company',
            'wechatid','weiboid','qqid','appleUUID','deviceID',
            'facebookid','twitterid','douyinid','ticktokid','googleid',
            'status','realstatus',
        ]

    def fields_public_list(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'country','province','city','company',
            'status','realstatus',
        ]

    def fields_overview(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'country','province','city','company',
            'status','realstatus',
        ]

    def fields_public_overview(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'country','province','city','company',
            'status','realstatus',
        ]

    def fields_search(self) -> list[str] | None:
        return [
            'userid','realname',
            'country','province','city','company',
        ]

    def fields_filter(self) -> list[str] | None:
        return [
            'userid','vip','vipexpire',
            'country','province','city','company',
            'wechatid','weiboid','qqid','appleUUID','deviceID',
            'facebookid','twitterid','douyinid','ticktokid','googleid',
            'status','realstatus',
        ]


    def fields_auto_convert(self) -> list[str] | None:
        return [
            'gallery',
            'vip','vipexpire',
            'createtime','lasttime',
        ]


    def table_def(self) -> list[AsDBFieldDef] | None:
        return [
            AsDBFieldDef.create('userid', '用户ID 唯一索引', DBFieldType.DBField_String, 8, False, DBFieldIndex.DBIndex_Unique),
            AsDBFieldDef.create('gallery', '相册 JSON ARRAY', DBFieldType.DBField_Json, -1, True, DBFieldIndex.DBIndex_None),

            AsDBFieldDef.create('vip', '是否vip', DBFieldType.DBField_Int, 2, False, DBFieldIndex.DBIndex_Index),
            AsDBFieldDef.create('vipexpire', 'vip过期时间', DBFieldType.DBField_Int, 11, False, DBFieldIndex.DBIndex_Index),

            AsDBFieldDef.create('realname', '真实姓名 30字以内', DBFieldType.DBField_String, 63, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('idnumber', '身份证号 30字以内', DBFieldType.DBField_String, 63, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('country', '国家 12字以内', DBFieldType.DBField_String, 24, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('province', '省份 12字以内', DBFieldType.DBField_String, 24, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('city', '城市 12字以内', DBFieldType.DBField_String, 24, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('company', '公司 30字以内', DBFieldType.DBField_String, 63, True, DBFieldIndex.DBIndex_None),

            AsDBFieldDef.create('wechatid', '微信公众平台openid 默认获取 unionid', DBFieldType.DBField_String, 32, True, DBFieldIndex.DBIndex_Unique),
            AsDBFieldDef.create('weiboid', '微博ID', DBFieldType.DBField_String, 63, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('appleUUID', '苹果UUID', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('facebookid', 'facebook', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('twitterid', 'twitter', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('googleid', 'google', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('douyinid', '抖音id', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('ticktokid', 'ticktokid', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('qqid', 'qqID', DBFieldType.DBField_String, 63, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('deviceid', 'Device ID', DBFieldType.DBField_String, 64, True, DBFieldIndex.DBIndex_None),
            AsDBFieldDef.create('realstatus', '实名状态 ', DBFieldType.DBField_String, 24, False, DBFieldIndex.DBIndex_None),

            common_db_fields()
        ]
