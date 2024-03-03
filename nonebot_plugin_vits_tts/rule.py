import asyncio
import re
import time

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.typing import T_State

from .config import config
from .utils.lang_id import get_lang
from .utils.model import get_model_from_speaker
from .vits.language import Language


class GroupState:
    def __init__(self, group_id: int):
        self.lock = asyncio.Lock()
        self.group_id: int = group_id
        self.last_run_time: int = 0

    async def update_time(self):
        async with self.lock:
            self.last_run_time = time.time()

    @property
    def is_cooldown(self):
        return (int(time.time()) - self.last_run_time) < config.cooldown


class Groups:
    def __init__(self):
        self.groups: dict[int, GroupState] = {}
        self.lock = asyncio.Lock()

    async def get(self, group_id) -> GroupState:
        if not self.groups.get(group_id):
            async with self.lock:
                self.groups[group_id] = GroupState(group_id)
        return self.groups.get(group_id)


groups = Groups()


def remove_cq_at(text: str) -> str:
    pattern = re.compile(r'\[CQ:at,qq=\d+]')
    return re.sub(pattern, '', text).strip()


async def is_tts_msg(bot: Bot, event: GroupMessageEvent, state: T_State) -> bool:
    if config.at_bot and (not event.to_me):
        return False
    group_state = await groups.get(event.group_id)

    pattern = re.compile(r"^(.*)说(.*)")
    match = pattern.search(str(event.raw_message))
    if not match:
        return False
    speaker = remove_cq_at(match.group(1))
    if not get_model_from_speaker(speaker):
        await bot.send(event=event, message=f"不支持的speaker：{speaker}")
        return False
    text = match.group(2).strip()
    lang = await get_lang(text)

    if not isinstance(lang, Language):
        await bot.send(event=event, message=f"不支持的语言：{lang}")
        return False

    state['vits_speaker'] = speaker
    state['vits_text'] = text
    state['vits_lang'] = lang

    if group_state.is_cooldown:
        await bot.send(event=event, message=f"太快啦，请等待一会再发送指令")
        return False
    await group_state.update_time()
    return True
