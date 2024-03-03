import pathlib

try:
    from nonebot import get_plugin_config
except ImportError:
    from nonebot import get_driver
from pydantic import BaseModel

try:
    from pydantic import field_validator
except ImportError:
    from pydantic import validator as field_validator


class _ScopedConfig(BaseModel):
    device: int = 0
    vmodel_path: str = 'models'
    at_bot: bool = False
    cooldown: int = 0
    vmodel_file_name: str = "model.pth"
    config_file_name: str = "config.pth"
    tencent_secret_id: str = ""
    tencent_secret_key: str = ""
    default_length_scale: float = 1
    default_noise_scale: float = .667
    default_noise_scale_w: float = .6

    @field_validator("vmodel_path")
    @classmethod
    def get_model_path(cls, value):
        return pathlib.Path(value)


class Config(BaseModel):
    vits: _ScopedConfig = _ScopedConfig()


try:
    # pydantic v2
    config = get_plugin_config(Config).vits
except:
    # pydantic v1
    config = Config.parse_obj(get_driver().config).vits
