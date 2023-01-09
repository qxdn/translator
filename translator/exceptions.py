class TranslationException(Exception):
    ...


class EncodingNotSupportException(TranslationException):
    def __init__(self, encoding: str, *args: object, **kwargs) -> None:
        super().__init__(encoding, *args)
        self.encoding = encoding

    def __repr__(self) -> str:
        return f"encoding {self.encoding} is not support"


class NotTranslationResultException(TranslationException):
    ...


class YoudaoTranslationException(TranslationException):
    """
    TODO ERROR CODE
    """

    def __init__(self, result: dict, *args: object) -> None:
        super().__init__(result, *args)
        self.result = result

    def __repr__(self) -> str:
        return f"youdao error:{self.result}"


class TencentTranslationException(TranslationException):
    def __init__(self, e, *args: object) -> None:
        super().__init__(e, *args)
        self.e = e

    def __repr__(self) -> str:
        return f"tencent error{self.e}"


class BaiduTranslationException(TranslationException):
    """
    TODO ERROR CODE
    """

    def __init__(self, result: dict, *args: object) -> None:
        super().__init__(result, *args)
        self.result = result

    def __repr__(self) -> str:
        return f"baidu error:{self.result}"


class TokenExpiredException(TranslationException):
    def __init__(self, result, *args: object) -> None:
        super().__init__(result, *args)
        self.result = result

    def __repr__(self) -> str:
        return f"token expired:{self.result}"


class TranslatorNotFoundException(TranslationException):
    def __init__(self, name: str, *args: object) -> None:
        super().__init__(name, *args)
        self.name = name

    def __repr__(self) -> str:
        return f"translator {self.name} not found"