from setuptools import setup

APP = ['mycolors.py']
# DATA_FILES = ['1.gif', '2.gif']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'logo.icns',
    'argv_emulation': True,
    'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)