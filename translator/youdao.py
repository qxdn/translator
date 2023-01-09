from .translators import BaseTranslator
from .encodings import TranslationEncoding
from .exceptions import YoudaoTranslationException
from .utils import overrides,translators_register

import hashlib
import time 
import uuid
import httpx

@translators_register()
class YoudaoTranslator(BaseTranslator):
    
    _encoding_dict:dict = {
        TranslationEncoding.AUTO: 'auto',
        TranslationEncoding.SIMPLE_CHINESE: 'zh-CHS',
        TranslationEncoding.JAPANESE: 'ja',
        TranslationEncoding.ENGLISH: 'en'
    }

    def __init__(self, app_key:str,app_secret:str,base_url:str='https://openapi.youdao.com/api',**kwargs) -> None:
        self.base_url = base_url
        self.app_key:str = app_key
        self.app_secret:str = app_secret
    
    def _truncate(self,q:str):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def _encrypt(self,sign_str:str):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(sign_str.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def _request_body(self,text: str, src, target,**kwargs):
        '''
        https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html#section-6
        '''
        body = {}
        body['q'] = text
        body['from'] = self.encoding_transform(src)
        body['to'] = self.encoding_transform(target)
        body['appKey'] = self.app_key
        body['signType'] = 'v3'
        curtime = str(int(time.time()))
        body['curtime'] = curtime
        salt = str(uuid.uuid1())
        sign_str = self.app_key + self._truncate(text) + salt + curtime + self.app_secret
        sign = self._encrypt(sign_str)
        body['salt'] = salt
        body['sign'] = sign
        return body

    @overrides(BaseTranslator)
    def translate(self,text: str, src=TranslationEncoding.AUTO, target=TranslationEncoding.SIMPLE_CHINESE, **kwargs):
        body = self._request_body(text,src,target)
        resp = httpx.post(self.base_url,data=body)
        data:dict = resp.json()
        if data["errorCode"] != "0":
            raise YoudaoTranslationException(data)       
        return data['translation'][0]
    
    @classmethod
    @overrides(BaseTranslator)
    def name(cls)->str:
        return "youdao"
