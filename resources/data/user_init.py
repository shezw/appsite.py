from engine.utils.Constants import DBSuperAdminUID, DBAdminUID, UserGroup, DBStatus, DBDefaultSASSID
from flask_babel import gettext as _

user_init_data = [
    {
        "saasid": DBDefaultSASSID,
        "uid": DBSuperAdminUID,
        "username": "superadmin",
        "nickname": _("Super Admin"),
        "groupid": UserGroup.SuperAdmin,
        "status": DBStatus.Super,
        "userid": DBSuperAdminUID,
        "avatar": "/static/images/avatar/default.png",
    },
    {
        "saasid": DBDefaultSASSID,
        "uid": DBAdminUID,
        "username": "admin",
        "nickname": _("Admin"),
        "groupid": UserGroup.Admin,
        "status": DBStatus.Enabled,
        "userid": "admin",
        "avatar": "/static/images/avatar/default.png",
    },
    {
        "saasid": DBDefaultSASSID,
        "uid": "00000000",
        "username": "demo_user",
        "nickname": _("Demo User"),
        "groupid": UserGroup.Registered,
        "status": DBStatus.Enabled,
        "userid": "demo_user",
        "avatar": "/static/images/avatar/default.png",
    }
]

group_init_data = [

]