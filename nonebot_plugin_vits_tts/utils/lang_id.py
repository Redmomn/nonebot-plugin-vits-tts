import json
import logging

from langdetect import detect
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import tmt_client, models

from ..config import config
from ..vits.language import Language

logging.basicConfig(level=logging.INFO)
use_tencent_tmt = False
if config.tencent_secret_key and config.tencent_secret_id:
    try:
        cred = credential.Credential(config.tencent_secret_id, config.tencent_secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"
        httpProfile.req
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)
        use_tencent_tmt = True
    except:
        pass


async def get_lang(text: str) -> Language | str:
    if use_tencent_tmt:
        try:
            return await _get_lang_by_tencent_tmt(text)
        except:
            return await _get_lang_by_langdetect(text)
    return await _get_lang_by_langdetect(text)


async def _get_lang_by_tencent_tmt(text: str) -> Language | str:
    try:
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.LanguageDetectRequest()
        params = {
            "Text": text,
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个LanguageDetectResponse的实例，与请求对象对应
        resp = client.LanguageDetect(req)
        # 输出json格式的字符串回包
        lang = json.loads(resp.to_json_string()).get("Lang")
        if lang == 'zh':
            return Language.ZH_CN
        elif lang == 'en':
            return Language.EN
        elif lang == 'jp':
            return Language.JP
        else:
            return lang

    except TencentCloudSDKException as err:
        raise err


async def _get_lang_by_langdetect(text: str) -> Language | str:
    lang = detect(text)
    if lang == 'zh-cn':
        return Language.ZH_CN
    elif lang == 'en':
        return Language.EN
    elif lang == 'ja':
        return Language.JP
    else:
        return lang
