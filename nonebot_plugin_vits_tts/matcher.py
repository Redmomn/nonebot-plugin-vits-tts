from nonebot import on_regex, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.log import logger
from nonebot.rule import Rule
from nonebot.typing import T_State

from .rule import is_tts_msg
from .utils.audio import wav_to_mp3
from .utils.model import get_model_from_speaker, speakers
from .vits import generate_voice

vits_req = on_regex(r"^(.*)说(.*)", rule=Rule(is_tts_msg))
help_req = on_command("help", aliases={"帮助", "语音帮助", "语音合成帮助"})


@vits_req.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    speaker = state.get("vits_speaker")
    text = state.get("vits_text")
    lang = state.get("vits_lang")

    model = get_model_from_speaker(speaker)
    logger.info(f"使用模型{model.model_name}.{speaker}生成语音：{text}")

    audio = await wav_to_mp3(await generate_voice(model_path=str(model.model),
                                                  config_path=str(model.config),
                                                  language=lang,
                                                  text=text,
                                                  spk=speaker))
    await vits_req.finish(message=MessageSegment.record(file=audio))


@help_req.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = '发送"[角色名]说[要合成的内容]"即可\n例如：宁宁说私のオナニを見てください\n目前支持以下角色的语音合成：\n'
    for r in speakers:
        msg += r + ' '
    await help_req.finish(msg)
