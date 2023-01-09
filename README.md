# tranlator
多个机翻api的集合

# usage
see `example`

## translate
```python
from translator.baidu import BaiduTranslator
from translator.exceptions import TranslationException
from translator.encodings import TranslationEncoding
from translator.utils import translators


TEXT = 'YOUR TEXT'
APIKEY = "YOUR API KEY"
SECERTKEY = "YOUR SECERTKEY"
trans = BaiduTranslator(APIKEY,SECERTKEY)
# or like below
#trans = translators('baidu',APIKEY,SECERTKEY)


try:
    print(trans.translate(TEXT))
except TranslationException as e:
    print(e)
```
## custom translator
```python
from translator.utils import translators_register,translators
from translator.translators import BaseTranslator
from translator.encodings import TranslationEncoding


@translators_register()
class CustomTranslator(BaseTranslator):

    _encoding_dict:dict = {
        TranslationEncoding.AUTO:"auto",
        TranslationEncoding.SIMPLE_CHINESE: "zh",
        # ...
    } 

    def __init__(self, **kwargs) -> None:
        ...
    
    def translate(self, text: str, src=TranslationEncoding.AUTO, target=TranslationEncoding.SIMPLE_CHINESE, **kwargs):
        return f"src text:{text},src encoding:{self.encoding_transform(src)},target encoding:{self.encoding_transform(target)}"



if __name__ == '__main__':
    a = CustomTranslator()
    print(a.translate("sss"))
    # or
    b = translators("CustomTranslator")
    print(b.translate("ccc"))

```
