from .encodings import TranslationEncoding
from .translators import BaseTranslator
from .exceptions import TencentTranslationException
from .utils import overrides,translators_register

import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

@translators_register()
class TencentTranslator(BaseTranslator):

    _encoding_dict:dict = {
        TranslationEncoding.AUTO: 'auto',
        TranslationEncoding.ENGLISH: 'en',
        TranslationEncoding.SIMPLE_CHINESE: 'zh',
        TranslationEncoding.JAPANESE: 'ja'
    }

    def __init__(self,secret_id:str, secret_key:str,region:str='ap-shanghai',**kwargs) -> None:
        self.cred = credential.Credential(secret_id, secret_key)
        self._region = region
        self.client = tmt_client.TmtClient(self.cred,self._region)
    
    @property
    def region(self) ->str:
        return self._region

    @region.setter
    def region(self,value):
        # TODO lock
        self._region = value
        self.client = tmt_client.TmtClient(self.cred,self.region)

    def _request_body(self,text: str, src, target,project_id:str=0,untranslated_text:str=None, **kwargs):
        '''
        
        '''
        body = {}
        body['SourceText'] = text
        body['Source'] = self.encoding_transform(src)
        body['Target'] = self.encoding_transform(target)
        body['ProjectId'] = project_id
        body['UntranslatedText'] = untranslated_text
        return body

    @overrides(BaseTranslator)
    def translate(self, text: str, src=TranslationEncoding.AUTO, target=TranslationEncoding.SIMPLE_CHINESE,project_id:str=0,untranslated_text:str=None, **kwargs):
        try:
            req = models.TextTranslateRequest()
            params = self._request_body(text,src,target,project_id,untranslated_text)
            req.from_json_string(json.dumps(params))     
            # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
            resp = self.client.TextTranslate(req)
        except TencentCloudSDKException as err:
            raise TencentTranslationException(err)

        return resp.TargetText 
    
    @classmethod
    @overrides(BaseTranslator)
    def name(cls)->str:
        return "tencent"