from enum import Enum
import time
from gettext import gettext as _
from flask_babel import ngettext as n_, ngettext  # type: ignore

class AsTimeConstants(int):
    CENTURY = 3155692600*1000  # 百年
    YEAR = 31556926*1000  # 一年
    THIRTY = 2592000*1000  # 30天
    WEEK = 604800*1000  # 一周
    DAY = 86400*1000  # 一天
    HOUR = 3600*1000  # 一小时
    HALF_HOUR = 1800*1000  # 半小时
    MINUTE = 60*1000  # 一分钟
    SECOND = 1*1000  # 一秒
    MILLISECOND = 1  # 一毫秒


class AsTimeFormat(Enum):
    LiteDate = 'litedate'
    FullDate = 'fulldate'
    NumberDate = 'numberdate'
    LiteTime = 'litetime'
    FullTime = 'fulltime'
    NumberTime = 'numbertime'
    NumberMonth = 'numbermonth'
    DatePicker = 'datepicker'


class AsTime:
    def __init__(self, specific_time_ms: int = 0):
        # 当前时间戳 单位: 毫秒
        self.now = int(time.time() * 1000)
        self.time = self.now

        if specific_time_ms > 0:
            self.time = specific_time_ms

    @staticmethod
    def from_str_cn(time_str: str):
        # 解析中文时间字符串，返回对应的时间戳（毫秒）
        # Parse Chinese time string and return the corresponding timestamp in milliseconds
        units = {
            '年': AsTimeConstants.YEAR,
            '个月': AsTimeConstants.THIRTY,
            '月': AsTimeConstants.THIRTY,
            '周': AsTimeConstants.WEEK,
            '天': AsTimeConstants.DAY,
            '日': AsTimeConstants.DAY,
            '小时': AsTimeConstants.HOUR,
            '时': AsTimeConstants.HOUR,
            '分钟': AsTimeConstants.MINUTE,
            '分': AsTimeConstants.MINUTE,
            '秒': AsTimeConstants.SECOND,
            '毫秒': AsTimeConstants.MILLISECOND
        }

        total_ms = 0
        num = ''
        for char in time_str:
            if char.isdigit():
                num += char
            else:
                if num and char in units:
                    total_ms += int(num) * units[char]
                    num = ''
        return total_ms

    @staticmethod
    def from_str_en(time_str: str):
        # 解析英文时间字符串，返回对应的时间戳（毫秒）
        # Parse English time string and return the corresponding timestamp in milliseconds
        units = {
            _('year'): AsTimeConstants.YEAR,
            _('years'): AsTimeConstants.YEAR,
            _('month'): AsTimeConstants.THIRTY,
            _('months'): AsTimeConstants.THIRTY,
            _('week'): AsTimeConstants.WEEK,
            _('weeks'): AsTimeConstants.WEEK,
            _('day'): AsTimeConstants.DAY,
            _('days'): AsTimeConstants.DAY,
            _('hour'): AsTimeConstants.HOUR,
            _('hours'): AsTimeConstants.HOUR,
            _('minute'): AsTimeConstants.MINUTE,
            _('minutes'): AsTimeConstants.MINUTE,
            _('second'): AsTimeConstants.SECOND,
            _('seconds'): AsTimeConstants.SECOND,
            _('millisecond'): AsTimeConstants.MILLISECOND,
            _('milliseconds'): AsTimeConstants.MILLISECOND
        }

        total_ms = 0
        parts = time_str.split()
        i = 0
        while i < len(parts):
            if parts[i].isdigit() and i + 1 < len(parts) and parts[i + 1] in units:
                total_ms += int(parts[i]) * units[parts[i + 1]]
                i += 2
            else:
                i += 1
        return total_ms

    def is_am(self):
        # 判断当前时间是否为上午
        # check if current time is AM
        local_time = time.localtime(self.time / 1000)
        return local_time.tm_hour < 12

    def this_day(self):
        # 获取当天的开始时间戳（毫秒）
        # get this day start time
        local_time = time.localtime(self.time / 1000)
        start_of_day = time.mktime((local_time.tm_year, local_time.tm_mon, local_time.tm_mday, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_day * 1000)

    def today(self):
        # 获取今天的开始时间戳（毫秒）
        # get today start time
        return self.this_day()

    def last_day(self):
        # 获取昨天的开始时间戳（毫秒）
        # get last day start time
        return self.this_day() - AsTimeConstants.DAY

    def yesterday(self):
        # 获取昨天的开始时间戳（毫秒）
        # get yesterday start time
        return self.last_day()

    def next_day(self):
        # 获取明天的开始时间戳（毫秒）
        # get next day start time
        return self.this_day() + AsTimeConstants.DAY

    def tomorrow(self):
        # 获取明天的开始时间戳（毫秒）
        # get tomorrow start time
        return self.next_day()

    def this_month(self):
        # 获取本月的开始时间戳（毫秒）
        # get this month start time
        local_time = time.localtime(self.time / 1000)
        start_of_month = time.mktime((local_time.tm_year, local_time.tm_mon, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_month * 1000)

    def last_month(self):
        # 获取上月的开始时间戳（毫秒）
        # get last month start time
        local_time = time.localtime(self.time / 1000)
        year = local_time.tm_year
        month = local_time.tm_mon - 1
        if month == 0:
            month = 12
            year -= 1
        start_of_last_month = time.mktime((year, month, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_last_month * 1000)

    def next_month(self):
        # 获取下月的开始时间戳（毫秒）
        # get next month start time
        local_time = time.localtime(self.time / 1000)
        year = local_time.tm_year
        month = local_time.tm_mon + 1
        if month == 13:
            month = 1
            year += 1
        start_of_next_month = time.mktime((year, month, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_next_month * 1000)

    def this_year(self):
        # 获取今年的开始时间戳（毫秒）
        # get this year start time
        local_time = time.localtime(self.time / 1000)
        start_of_year = time.mktime((local_time.tm_year, 1, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_year * 1000)

    def last_year(self):
        # 获取去年的开始时间戳（毫秒）
        # get last year start time
        local_time = time.localtime(self.time / 1000)
        start_of_last_year = time.mktime((local_time.tm_year - 1, 1, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_last_year * 1000)

    def next_year(self):
        # 获取明年的开始时间戳（毫秒）
        # get next year start time
        local_time = time.localtime(self.time / 1000)
        start_of_next_year = time.mktime((local_time.tm_year + 1, 1, 1, 0, 0, 0, local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst))
        return int(start_of_next_year * 1000)

    def week_day(self):
        # 获取当前所处的周几
        # get the day of the week, 0 is Monday, 6 is Sunday
        local_time = time.localtime(self.time / 1000)
        return local_time.tm_wday

    def days(self):
        # 获取当前时间是本月的第几天
        # get the day of the month
        local_time = time.localtime(self.time / 1000)
        return local_time.tm_mday

    def month(self):
        # 获取当前时间是本年的第几月
        # get the month of the year
        local_time = time.localtime(self.time / 1000)
        return local_time.tm_mon

    def year(self):
        # 获取当前时间是第几年
        # get the year
        local_time = time.localtime(self.time / 1000)
        return local_time.tm_year

    def is_yesterday(self):
        # 判断当前时间是否为昨天
        # check if current time is yesterday
        return self.yesterday() <= self.time < self.today()

    def is_before_today(self):
        # 判断当前时间是否为今天之前
        # check if current time is before today
        return self.time < self.today()

    def is_today(self):
        # 判断当前时间是否为今天
        # check if current time is today
        return self.today() <= self.time < self.tomorrow()

    def is_after_today(self):
        # 判断当前时间是否为今天之后
        # check if current time is after today
        return self.time >= self.tomorrow()

    def is_tomorrow(self):
        # 判断当前时间是否为明天
        # check if current time is tomorrow
        return self.tomorrow() <= self.time < self.next_day() + AsTimeConstants.DAY

    def is_this_month(self):
        # 判断当前时间是否为本月
        # check if current time is this month
        return self.this_month() <= self.time < self.next_month()

    def is_last_month(self):
        # 判断当前时间是否为上月
        # check if current time is last month
        return self.last_month() <= self.time < self.this_month()

    def is_next_month(self):
        # 判断当前时间是否为下月
        # check if current time is next month
        return self.next_month() <= self.time < self.next_month() + AsTimeConstants.THIRTY

    def format_output(self,format_str: str = "%Y-%m-%d %H:%M:%S"):
        # 格式化输出时间字符串
        # format output time string
        local_time = time.localtime(self.time / 1000)
        return time.strftime(format_str, local_time)

    def natural_language(self):
        # 获取自然语言描述的时间差
        # get natural language description of time difference

        diff = self.now - self.time

        if diff < -AsTimeConstants.YEAR:
            return f"{ngettext('%(num)d year from now', '%(num)d years from now', -diff // AsTimeConstants.YEAR)}"
        elif diff < -AsTimeConstants.THIRTY:
            return f"{ngettext('%(num)d month from now', '%(num)d months from now', -diff // AsTimeConstants.THIRTY)}"
        elif diff < -AsTimeConstants.WEEK:
            return f"{ngettext('%(num)d week from now', '%(num)d weeks from now', -diff // AsTimeConstants.WEEK)}"
        elif diff < -AsTimeConstants.DAY:
            return f"{ngettext('%(num)d day from now', '%(num)d days from now', -diff // AsTimeConstants.DAY)}"
        elif diff < -AsTimeConstants.HOUR:
            return f"{ngettext('%(num)d hour from now', '%(num)d hours from now', -diff // AsTimeConstants.HOUR)}"
        elif diff < -AsTimeConstants.MINUTE:
            return f"{ngettext('%(num)d minute from now', '%(num)d minutes from now', -diff // AsTimeConstants.MINUTE)}"
        elif diff < -AsTimeConstants.SECOND:
            return f"{ngettext('%(num)d second from now', '%(num)d seconds from now', -diff // AsTimeConstants.SECOND)}"
        elif diff < AsTimeConstants.MINUTE:
            return f"{ngettext('%(num)d second ago', '%(num)d seconds ago', diff // AsTimeConstants.SECOND)}"
        elif diff < AsTimeConstants.HOUR:
            return f"{ngettext('%(num)d minute ago', '%(num)d minutes ago', diff // AsTimeConstants.MINUTE)}"
        elif diff < AsTimeConstants.DAY:
            return f"{ngettext('%(num)d hour ago', '%(num)d hours ago', diff // AsTimeConstants.HOUR)}"
        elif diff < AsTimeConstants.WEEK:
            return f"{ngettext('%(num)d day ago', '%(num)d days ago', diff // AsTimeConstants.DAY)}"
        elif diff < AsTimeConstants.THIRTY:
            return f"{ngettext('%(num)d week ago', '%(num)d weeks ago', diff // AsTimeConstants.WEEK)}"
        elif diff < AsTimeConstants.YEAR:
            return f"{ngettext('%(num)d month ago', '%(num)d months ago', diff // AsTimeConstants.THIRTY)}"
        elif diff >= AsTimeConstants.YEAR:
            return f"{n_('%(num)d year ago', '%(num)d years ago', diff // AsTimeConstants.YEAR)}"
        else:
            return _("just now")
