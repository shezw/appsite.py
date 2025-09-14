from core.utils.Time import AsTime

class AsResult:
    def __init__(self):
        self.code = 0
        self.message = ''
        self.content = None
        self.last = 'unknown'
        self.time = AsTime()

    @staticmethod
    def construct(code=0, message=None, content=None, last='unknown', time=0):
        result = AsResult()
        result.code = code
        result.message = message
        result.content = content
        result.last = last
        result.time = AsTime(specific_time_ms=time)
        return result

    def is_success(self):
        return self.code == 0

    def get_code(self):
        return self.code

    def get_content_or(self, default_val=None):
        if self.is_success():
            return self.content
        return default_val

    def get_last(self):
        return self.last

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'content': self.content,
            'last': self.last,
            'time': self.time.time
        }

    def to_string(self):
        return str(self.to_dict())

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

