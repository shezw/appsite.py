from enum import Enum, IntEnum

DBSuperAdminUID = "SUPER"
DBAdminUID = "ADMIN"

DBDefaultSASSID = "DEFAULT"

class UserGroup(Enum):
    SuperAdmin = '900'
    Admin = '800'
    Editor = '400'
    Author = '300'
    AuthorStandard = '3010'
    AuthorPro = '3020'
    AuthorExclusive = '3030'
    Registered = '100'
    Guest = '0'
    Illegal = '00000000'


class UserGroupLevel(IntEnum):
    SuperAdmin = 90000
    Admin = 80000
    Editor = 40000
    Author = 30000
    AuthorStandard = 30100
    AuthorPro = 30200
    AuthorExclusive = 30300
    Registered = 10000
    Guest = 0
    Illegal = -1


class UserGroupRole(Enum):
    Guest = 'guest'
    User = 'user'
    Manager = 'manager'
    Super = 'super'
    Editor = 'editor'
    Illegal = 'illegal'


class DBStatus(Enum):
    Super = 'SUPER'
    Enabled = 'enabled'
    Disabled = 'disabled'
    Offline = 'offline'
    Trash = 'trash'
    Pending = 'pending'
    Blocked = 'blocked'
    Locked = 'locked'
    Default = 'default'
    Verified = 'verified'
    Sent = 'sent'
    Received = 'received'
    Read = 'read'
    Success = 'success'
    Failed = 'failed'
    Error = 'error'


class DBContentType(Enum):
    Email = 'email'
    EmailSubject = 'subject'
    SMS = 'sms'
    HTML = 'html'
    Message = 'message'
    Notify = 'notify'
    Common = 'common'
    Normal = 'normal'
    Media = 'media'
    Image = 'image'
    Audio = 'audio'
    Video = 'video'
    Article = 'article'
    Url = 'url'
    File = 'file'
    Product = 'product'
    Page = 'page'
    Website = 'website'
    Item = 'item'
    Payment = 'payment'
    Commission = 'commission'  # 佣金
    Transmission = 'transmission'  # 转账
    Bonus = 'bonus'  # 奖励
    Balance = 'balance'  # 余额
    Point = 'point'  # 积分


