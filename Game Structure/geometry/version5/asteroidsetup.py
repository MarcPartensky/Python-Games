from setuptools import setup


APP = ['myasteroidgame.py', "myabstract.py", "mybody.py", "myanatomies.py", "myentity.py", "myspaceship.py",
       "myspaceshipgroup.py","mymotion.py", "myrectangle.py", "myrect.py", "mycontext.py", "mywindow.py", "myplane.py",
       "mydraw.py", "mycollider.py", "mymanager.py", "mycolors.py", "myentitygroup.py", "mygroup.py", "mygame.py",
       "mymaterial.py", "myphysics.py"]
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