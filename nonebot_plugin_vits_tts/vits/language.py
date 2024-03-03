from enum import Enum


class Language(Enum):
    # 日语
    JP = "[JA]"
    # 简体中文
    ZH_CN = "[ZH]"
    # 英文
    EN = "[EN]"

    def __add__(self, other) -> str:
        return self.value + str(other)

    def __radd__(self, other) -> str:
        return str(other) + self.value
