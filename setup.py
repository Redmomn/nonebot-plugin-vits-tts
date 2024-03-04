from setuptools import setup, find_packages

setup(
    name='nonebot_plugin_vits_tts',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'torchaudio',
        'numpy>=1.22.0',
        'scipy',
        'regex',
        'cn2an',
        'opencc',
        'inflect',
        'unidecode',
        'eng_to_ipa',
        'pyopenjtalk-prebuilt',
        'jamo',
        'ko_pron',
        'pypinyin',
        'jieba',
        'indic_transliteration',
        'num_thai',
        'pydub',
        'numba',
        'tencentcloud-sdk-python-tmt',
        'langdetect',
        'nonebot-adapter-onebot>=2.0.0',
        'nonebot2>=2.0.0'
    ],
    author='Redmomn',
    author_email='109732988+Redmomn@users.noreply.github.com',
    description='nonebot-plugin-vits-tts',
    long_description=open('README.md', encoding='utf*8').read(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    keywords=['nonebot2', 'vits', 'tts'],
    url='https://github.com/Redmomn/nonebot-plugin-vits-tts'
)
