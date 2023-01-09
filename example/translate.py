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