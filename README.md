<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-vits-tts

✨ 基于vits的nonebot语音合成插件 ✨

<p align="center">
  <a href="https://github.com/Redmomn/nonebot-plugin-vits-tts/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Redmomn/nonebot-plugin-vits-tts.svg" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <a href="https://pypi.org/project/nonebot-plugin-vits-tts">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-vits-tts" alt="pypi">
  </a>
</p>

</div>

## 📖 介绍

基于vits的tts语音生成，适配onebot v11协议  
已兼容pydantic v1&v2

## 💿 安装

<details open>
<summary>nb-cli</summary>

    nb plugin install nonebot-plugin-vits-tts

</details>

<details open>
<summary>pip</summary>

    pip install nonebot_plugin_vits_tts

</details>

## ⚙️ 配置

| 配置项                         | 类型    | 默认值       | 说明                                                                    |
|-----------------------------|-------|-----------|-----------------------------------------------------------------------|
| VITS__DEVICE                | int   | 0         | 使用指定的cuda设备进行tts合成，如果没有指定的显卡会自动使用cpu                                  |
| VITS__VMODEL_PATH           | str   | models    | 插件会读取此文件夹下的所有模型                                                       |
| VITS__AT_BOT                | bool  | false     | 使用语音合成是否需要@bot                                                        |
| VITS__COOLDOWN              | int   | 0         | 在每个群里生成语音的冷却时间，防止设备负载过大                                               |
| VITS__VMODEL_FILE_NAME      | str   | model.pth | 模型文件名                                                                 |
| VITS__CONFIG_FILE_NAME      | str   | config    | 模型配置文件                                                                |
| VITS__TENCENT_SECRET_ID     | str   |           | 腾讯云机器翻译SECRET_ID，用于语种识别                                               |
| VITS__TENCENT_SECRET_KEY    | str   |           | 腾讯云机器翻译SECRET_KEY，这两项不配置或者配置不正确会使用langdetect库进行语种识别，使用langdetect准确率较低 |
| VITS__DEFAULT_LENGTH_SCALE  | float | 1         | 整体语速                                                                  |
| VITS__DEFAULT_NOISE_SCALE   | float | 0.667     | 感情变化程度                                                                |
| VITS__DEFAULT_NOISE_SCALE_W | float | 0.6       | 音素发音长度                                                                |

假如你的项目配置是这样，则`VITS__VMODEL_PATH`应为`models`，`VITS__VMODEL_FILE_NAME`为`model.pth`，`VITS__CONFIG_FILE_NAME`
为`config.json`

```text
awsomebot
├─ .env
├─ .env.dev
├─ .env.prod
├─ .gitignore
├─ README.md
├─ models
│    ├─ model1
│    │    ├─ config.json
│    │    └─ model.pth
│    └─ model2
│           ├─ config.json
│           └─ model.pth
├─ pyproject.toml
└─ src
   └─ plugins
      └─ ...

```

**注意**  
所有的模型文件名应为`VITS__VMODEL_FILE_NAME`的值，配置文件名应为`VITS__CONFIG_FILE_NAME`的值，一个文件夹只允许放一个模型和配置文件，
不同模型使用文件夹分割开来，插件会自动加载所有文件夹下的模型

**使用cuda设备合成音频**

- 安装合适版本的[cuda-toolkit](https://developer.nvidia.com/cuda-toolkit)
- 需要手动安装GPU版本的pytorch，详见[Pytorch](https://pytorch.org/get-started/locally/)

## 🎉 使用

仅可以在群聊中使用  
使用方法：

- `[角色]说[要合成的文本]`  
  例如：

    - 宁宁说私のオナニを見てください
- 发送`/help` 可以获取可用角色列表

目前仅支持简体中文，日语，英文，插件会自动识别要合成文本的语种

## 模型分享

## 💡 感谢

- 此插件基于[Plachtaa/VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)的代码改进而来

## 关于模型训练

Plachtaa/VITS-fast-fine-tuning的[笔记本](https://colab.research.google.com/drive/1pn1xnFfdLK63gVXDwV4zCXfVeo8c-I-0?usp=sharing)  
另外还提供一个我改进过的[笔记本](https://colab.research.google.com/drive/1Uf-ngOqUiDXCPbsm122w56y6nuWiWcnu?usp=sharing)
，这个笔记本只保存最新的模型文件，不会将训练的中间文件保存到云盘导致云盘爆掉不能训练
