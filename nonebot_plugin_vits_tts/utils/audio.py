import os
import pathlib
import subprocess
import tempfile
import time
from io import BytesIO

from pydub import AudioSegment

# 获取系统临时文件夹路径
temp_folder = tempfile.gettempdir()


async def wav_to_mp3(wav_data: bytes) -> bytes:
    """
    wav格式转换为mp3
    :param wav_data: wav的二进制数据
    :return: mp3的二进制数据
    """
    input_file = pathlib.Path(os.path.join(temp_folder, f"{int(time.time() * 1000)}.wav"))
    input_file.write_bytes(wav_data)
    output_file = pathlib.Path(os.path.join(temp_folder, f"{int(time.time() * 1000)}.mp3"))
    subprocess.run(["ffmpeg", "-i", input_file, "-codec:a", "libmp3lame", "-q:a", "0", output_file])
    mp3_data = output_file.read_bytes()
    try:
        os.remove(input_file)
        os.remove(output_file)
    except:
        pass

    return mp3_data


async def wav_to_mp3_2(wav_file: bytes) -> bytes:
    """
    wav格式转换为mp3
    :param wav_file: wav的二进制数据
    :return: mp3的二进制数据
    """
    audio = AudioSegment.from_file(file=BytesIO(wav_file), format='wav')
    return audio.export(format='mp3').read()
