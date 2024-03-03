import io

import scipy.io.wavfile as wavf
import torch
from nonebot.log import logger
from torch import no_grad, LongTensor

from . import utils, commons
from .language import Language
from .models import SynthesizerTrn
from .text import text_to_sequence
from ..config import config

device = f"cuda:{config.device}" if torch.cuda.is_available() else "cpu"
logger.info(f"将使用设备{device}进行tts合成")


def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


async def generate_voice(model_path: str,
                         config_path: str,
                         language: Language,
                         text: str,
                         spk: str,
                         length_scale: float = config.default_length_scale,
                         noise_scale: float = config.default_noise_scale,
                         noise_scale_w: float = config.default_noise_scale_w) -> bytes:
    """
    生成语音，返回语音文件的bytes
    :param model_path: 模型路径
    :param config_path: 配置文件路径
    :param language: 语言
    :param text: 要合成的文本
    :param spk: 合成语音的角色名
    :param length_scale: 整体语速
    :param noise_scale: 感情变化程度
    :param noise_scale_w: 音素发音长度
    :return: wav音频文件的bytes
    """
    model_path = model_path
    config_path = config_path
    text = text
    spk = spk
    noise_scale = noise_scale
    noise_scale_w = noise_scale_w
    length_scale = length_scale

    hps = utils.get_hparams_from_file(config_path)
    net_g = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()
    _ = utils.load_checkpoint(model_path, net_g, None)

    speaker_ids = hps.speakers

    text = language + text + language
    speaker_id = speaker_ids[spk]
    stn_tst = get_text(text, hps, False)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(device)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
        sid = LongTensor([speaker_id]).to(device)
        audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                            length_scale=1.0 / length_scale)[0][0, 0].data.cpu().float().numpy()
    del stn_tst, x_tst, x_tst_lengths, sid

    file_obj = io.BytesIO()
    wavf.write(file_obj, hps.data.sampling_rate, audio)

    file_obj.seek(0)
    data = file_obj.read()
    with open('test.wav', mode='wb') as f:
        f.write(data)
    return data
