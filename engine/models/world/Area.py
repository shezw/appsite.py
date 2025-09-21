from engine.core.DB import AsDBFieldDef, DBFieldType, DBFieldIndex
from engine.utils.DBMS.DBTypes import common_db_fields, saas_db_field
from engine.core.Model import AsModel
from flask_babel import gettext as _

class AsArea(AsModel):

    def __init__(self):
        super().__init__()

    def table_name(self) -> str:
        return "area"

    def table_comment(self) -> str:
        return "The table for area information"

    def primary_key(self) -> str:
        return "uid"

    def enable_log(self) -> bool:
        return True

    def enable_redis_cache(self) -> bool:
        return True

    def fields_insert(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title','cover','description','gallery',
            'mergename','shortname','mergeshortname',
            'code','zipcode',
            'location','lng','lat',
            'level',
            'sort','featured','status','createtime','lasttime'
        ]

    def fields_update(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title','cover','description','gallery',
            'mergename','shortname','mergeshortname',
            'code','zipcode',
            'location','lng','lat',
            'level',
            'sort','featured','status','createtime','lasttime'
        ]

    def fields_detail(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title','cover','description','gallery',
            'mergename','shortname','mergeshortname',
            'code','zipcode',
            'lng','lat',
            'level',
            'sort','featured','status','createtime','lasttime'
        ]

    def fields_public_detail(self) -> list[str] | None:
        return [
            'uid','username','email','mobile','saasid',
            'nickname','avatar','cover','description','introduce',
            'birthday','gender','groupid','areaid','status','createtime','lasttime'
        ]

    def fields_list(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title','cover','description','gallery',
            'mergename','shortname','mergeshortname',
            'code','zipcode',
            'lng','lat',
            'level',
            'sort','featured','status','createtime','lasttime'
        ]

    def fields_public_list(self) -> list[str] | None:
        return [
            'uid','username','saasid',
            'nickname','avatar','description',
            'groupid','gender','areaid','status','createtime','lasttime'
        ]

    def fields_overview(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title','cover','description','gallery',
            'mergename','shortname','mergeshortname',
            'code','zipcode',
            'lng','lat',
            'level',
            'sort','featured','status','createtime','lasttime'
        ]

    def fields_public_overview(self) -> list[str] | None:
        return [
            'uid','username','saasid',
            'nickname','avatar','description',
            'groupid','areaid','createtime','lasttime'
        ]

    def fields_search(self) -> list[str] | None:
        return [
            'title'
        ]

    def fields_filter(self) -> list[str] | None:
        return [
            'uid','authorid','parentid',
            'title',
            'level',
            'location',
            'sort','featured','status','createtime','lasttime',
        ]

    def fields_auto_convert(self) -> list[str] | None:
        return [
            'level','sort','featured','lng','lat','gallery'
        ]


    def table_def(self) -> list[AsDBFieldDef] | None:
        return [
            saas_db_field(),

            AsDBFieldDef.create('uid', _('Area ID'), DBFieldType.String, 8, False, DBFieldIndex.Unique),
            AsDBFieldDef.create('authorid', _('Author ID'), DBFieldType.String, 8, True, DBFieldIndex.Index),
            AsDBFieldDef.create('parentid', _('Parent Area ID'), DBFieldType.String, 8, True, DBFieldIndex.Index),
            AsDBFieldDef.create('title', _('Area Title'), DBFieldType.String, 32, False),
            AsDBFieldDef.create('description', _('Area Description'), DBFieldType.String, 255, True),
            AsDBFieldDef.create('cover', _('Area Cover'), DBFieldType.String, 255, True),
            AsDBFieldDef.create('gallery', _('Area Gallery'), DBFieldType.Json, -1, True),
            AsDBFieldDef.create('mergename', _('Merged Name'), DBFieldType.String, 64, True),
            AsDBFieldDef.create('shortname', _('Short Name'), DBFieldType.String, 32, True),
            AsDBFieldDef.create('mergeshortname', _('Merged Short Name'), DBFieldType.String, 32, True),
            AsDBFieldDef.create('level', _('Area Level'), DBFieldType.Int, 3, True, DBFieldIndex.Index),
            AsDBFieldDef.create('code', _('Area Code'), DBFieldType.String, 12, True),
            AsDBFieldDef.create('zipcode', _('Zip Code'), DBFieldType.String, 12, True),
            AsDBFieldDef.create('location', _('Location'), DBFieldType.Location, -1, False, DBFieldIndex.Spatial),
            AsDBFieldDef.create('lng', _('Longitude'), DBFieldType.Decimal, 1410, False),
            AsDBFieldDef.create('lat', _('Latitude'), DBFieldType.Decimal, 1410, False),

            common_db_fields()
        ]

    def before_insert(self, data: dict) -> bool:
        # todo
        return True

    def before_update(self, data: dict) -> bool:
        # todo
        return True