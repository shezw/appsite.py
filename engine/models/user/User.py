from engine.core.DB import AsDBFieldDef, DBFieldType, DBFieldIndex, common_db_fields, saas_db_field
from engine.core.Model import AsModel
from engine.models.user.UserAccount import UserAccount
from engine.models.user.UserInfo import UserInfo


class User(AsModel):
    def __init__(self):
        super().__init__()

    def table_name(self) -> str:
        return "user"

    def table_comment(self) -> str:
        return "User Table"

    def primary_key(self) -> str:
        return "uid"

    def enable_log(self) -> bool:
        return True

    def enable_redis_cache(self) -> bool:
        return True

    def table_def(self) -> list[AsDBFieldDef] | None:
        return UserAccount().table_def().extend(UserInfo().table_def())

    def fields_insert(self) -> list[str] | None:
        return UserAccount().fields_insert().extend(UserInfo().fields_insert())

    def fields_update(self) -> list[str] | None:
        return UserAccount().fields_update().extend(UserInfo().fields_update())

    def fields_detail(self) -> list[str] | None:
        return UserAccount().fields_detail().extend(UserInfo().fields_detail())

    def fields_public_detail(self) -> list[str] | None:
        return UserAccount().fields_public_detail().extend(UserInfo().fields_public_detail())

    def fields_list(self) -> list[str] | None:
        return UserAccount().fields_list().extend(UserInfo().fields_list())

    def fields_public_list(self) -> list[str] | None:
        return UserAccount().fields_public_list().extend(UserInfo().fields_public_list())

    def fields_overview(self) -> list[str] | None:
        return UserAccount().fields_overview().extend(UserInfo().fields_overview())

    def fields_public_overview(self) -> list[str] | None:
        return UserAccount().fields_public_overview().extend(UserInfo().fields_public_overview())

    def fields_filter(self) -> list[str] | None:
        return UserAccount().fields_filter().extend(UserInfo().fields_filter())

    def fields_search(self) -> list[str] | None:
        return UserAccount().fields_search().extend(UserInfo().fields_search())

    def fields_auto_convert(self) -> list[str] | None:
        return UserAccount().fields_auto_convert().extend(UserInfo().fields_auto_convert())
