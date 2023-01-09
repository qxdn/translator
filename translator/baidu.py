from .translators import BaseTranslator
from .encodings import TranslationEncoding
from .utils import overrides,TTLDict,translators_register
from .exceptions import BaiduTranslationException,TokenExpiredException

import httpx
import json

MONTH = 60*60*24*30 

@translators_register()
class BaiduTranslator(BaseTranslator):
    
    _encoding_dict:dict = {
        TranslationEncoding.AUTO: 'auto',
        TranslationEncoding.ENGLISH: 'en',
        TranslationEncoding.JAPANESE: 'jp',
        TranslationEncoding.SIMPLE_CHINESE: 'zh'
    }

    def __init__(self,api_key:str,secret_key:str,base_url:str='https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1',access_url:str='https://aip.baidubce.com/oauth/2.0/token',**kwargs) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.access_url = access_url
        self.cache = TTLDict(default_ttl=MONTH)

    @property
    def access_token(self)->str:
        token = self.cache.get("token",None)
        if token is None:
            token = self.get_access_token()
        return token
    
    def get_access_token(self,url:str=None)->str:
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        if None == url:
            url = self.access_url
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        result:dict = httpx.post(url, params=params).json()
        if None != result.get('error',None):
            raise BaiduTranslationException(result)
        access_token = result['access_token']
        expired = result['expires_in']
        self.cache.set('token',access_token,expired)
        return access_token

    def _request_body(self,text: str, src, target, **kwargs):
        '''
        https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%B7%E6%B1%82%E8%AF%B4%E6%98%8E
        '''
        body = {}
        body['q'] = text
        body['from'] = self.encoding_transform(src)
        body['to'] = self.encoding_transform(target)
        return json.dumps(body)

    def _request_data(self,url:str,header:dict,data:dict):
        resp:dict = httpx.post(url,headers=header,data=data).json()
        error_code = resp.get('error_code',None)
        if error_code != None:
            if error_code == 111:
                raise TokenExpiredException(resp)
            else:
                raise BaiduTranslationException(resp)
        return resp

    @overrides(BaseTranslator)
    def translate(self, text: str, src=TranslationEncoding.AUTO, target=TranslationEncoding.SIMPLE_CHINESE, **kwargs):
        access_token = self.access_token
        url = f"{self.base_url}?access_token={access_token}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        body = self._request_body(text,src,target)

        try:
            resp = self._request_data(url,headers,body)
        except TokenExpiredException as exception:
            resp = self._request_data(url,headers,body)

        result = resp['result']['trans_result'][0]['dst']
        return result
    
    @classmethod
    @overrides(BaseTranslator)
    def name(cls)->str:
        return "baidu"