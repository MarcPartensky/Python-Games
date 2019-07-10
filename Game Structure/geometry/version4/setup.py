from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Window",
    version = "1",
    description = "Vive les fenetres",
    executables = [Executable("window.py")],
)

#Terminal:
#python setup.py build
#
