from nonebot.plugin import PluginMetadata

from .config import Config
from .matcher import vits_req, help_req

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-vits-tts",
    description="基于vits的tts语音合成",
    usage="[角色]说[要合成的文本]",
    type="application",
    homepage="https://github.com/Redmomn/nonebot-plugin-vits-tts",
    supported_adapters={"~onebot.v11"},
    config=Config,
    extra={"author": "Redmomn"}
)

__all__ = ["vits_req", "help_req"]
