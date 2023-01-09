
from enum import Enum

class TranslationEncoding(str,Enum):
    AUTO = "AUTO"
    SIMPLE_CHINESE = 'zh-cn'
    JAPANESE = "ja"
    ENGLISH = 'en'