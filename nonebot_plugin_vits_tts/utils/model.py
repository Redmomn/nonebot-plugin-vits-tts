import json
import os
import pathlib

from nonebot.log import logger

from ..config import config


class Model:
    def __init__(self, model_path: pathlib.Path, config_path: pathlib.Path):
        self.speakers: list[str] = []
        self.model = model_path
        self.config = config_path
        with config_path.open(mode='r', encoding='utf-8') as f:
            config_data: dict = json.load(f)
        for speaker in config_data.get("speakers"):
            self.speakers.append(speaker)
        logger.info(f"已加载vits模型{model_path}")

    @property
    def model_name(self) -> str:
        return os.path.basename(os.path.dirname(self.model))

    def __str__(self) -> str:
        result = ""
        for k, v in self.__dict__.items():
            result += f"{k}:{v}\n"
        return result


def load_model(model_path: pathlib.Path) -> list[Model]:
    """
    递归加载指定文件夹的所有模型和配置文件
    模型和配置文件的文件名在config中给出
    :param model_path:
    :return: 一个 list[Model]
    """
    _models: list[Model] = []
    for root, _dir, files in os.walk(model_path):
        if (config.vmodel_file_name in files) and (config.config_file_name in files):
            _models.append(
                Model(pathlib.Path(os.path.join(root, config.vmodel_file_name)),
                      pathlib.Path(os.path.join(root, config.config_file_name))))
    return _models


def get_all_speakers_models() -> dict[str, Model]:
    """
    获取一个speaker与model实例的映射表
    :return: 一个speaker为键，model为值的dict
    """
    _speakers_models: dict[str, Model] = {}
    for _model in models:
        for _speaker in _model.speakers:
            _speakers_models[_speaker] = _model
    return _speakers_models


def get_model_from_speaker(speaker: str) -> Model | None:
    """
    从speaker的名字获取对应的model实例，不存在则返回none
    :param speaker: 说话人名称
    :return: model
    """
    return speakers_models.get(speaker, None)


models = load_model(config.vmodel_path)
speakers_models = get_all_speakers_models()
speakers = speakers_models.keys()
