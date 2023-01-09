import abc
from .exceptions import EncodingNotSupportException
from .encodings import TranslationEncoding

class BaseTranslator(abc.ABC):

    _encoding_dict:dict = {}

    def __init__(self,**kwargs) -> None:
        super().__init__()
    
    @property
    def encoding_dict(self)->dict:
        return self._encoding_dict
    
    def encoding_transform(self,encoding)->str:
        '''
        转换encoding
        '''
        _encoding = self.encoding_dict.get(encoding,None)
        if None == _encoding:
            raise EncodingNotSupportException(encoding)
        return _encoding

    @abc.abstractmethod
    def translate(self,text:str,src = TranslationEncoding.AUTO,target = TranslationEncoding.SIMPLE_CHINESE,**kwargs):
        raise NotImplementedError()

    @classmethod
    def name(cls)->str:
        return cls.__name__
