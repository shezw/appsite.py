#
# 基础模型组件
# ASModel
#
# 模型抽象类、集成了数据库查询、数据转换、缓存、Redis访问等
# Abstract class, integrated database query, data conversion, cache, Redis access, etc.
#
# @package APS\core
#
from abc import ABC, abstractmethod

from engine.core.DB import AsDBFieldDef


class AsModel(ABC):
    def __init__(self):
        pass

    # 数据库表名
    # Database table name
    @property
    @abstractmethod
    def table_name(self) -> str:
        return "AbstractModel"

    # 数据库 注释
    # Database table comment
    @property
    @abstractmethod
    def table_comment(self) -> str:
        return "Abstract Model Table"

    # 主键
    # Primary key
    @staticmethod
    def primary_key(self) -> str:
        return "uid"

    # 是否开启日志
    # Whether to enable logs
    @staticmethod
    def enable_log(self) -> bool:
        return False

    # 是否自动开启Redis缓存
    # Whether to automatically enable Redis cache
    def enable_redis_cache(self) -> bool:
        return False

    # 数据库表定义
    # Database table definition
    @abstractmethod
    def table_def(self) -> list[AsDBFieldDef] | None:
        return None

    # 插入支持字段
    # supported fields for insert
    @abstractmethod
    def fields_insert(self) -> list[str] | None:
        return None

    # 更新支持字段
    # supported fields for update
    @abstractmethod
    def fields_update(self) -> list[str] | None:
        return None

    # 详情支持字段
    # supported fields for detail
    @abstractmethod
    def fields_detail(self) -> list[str] | None:
        return None

    # 开放详情支持字段
    # supported fields for public detail
    @abstractmethod
    def fields_public_detail(self) -> list[str] | None:
        return None

    # 列表支持字段
    # supported fields for list
    @abstractmethod
    def fields_list(self) -> list[str] | None:
        return None

    # 公开列表支持字段
    # supported fields for public list
    @abstractmethod
    def fields_public_list(self) -> list[str] | None:
        return None

    # 概览支持字段
    # supported fields for overview
    @abstractmethod
    def fields_overview(self) -> list[str] | None:
        return None

    # 公开概览支持字段
    # supported fields for public overview
    @abstractmethod
    def fields_public_overview(self) -> list[str] | None:
        return None

    # 搜索支持字段
    # supported fields for search
    @abstractmethod
    def fields_search(self) -> list[str] | None:
        return None

    # 过滤、计数支持字段
    # supported fields for filter and count
    @abstractmethod
    def fields_filter(self) -> list[str] | None:
        return None

    # 自动转换字段
    # auto convert fields
    @abstractmethod
    def fields_auto_convert(self) -> list[str] | None:
        return None
