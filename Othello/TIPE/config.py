#CASES=[0,1]

CASE_VIDE =   -1   #Ne pas mettre 0 ou 1
DEBUGING  = True
INFO      = True

#import sys

"""
def debug(*txt) :
    if DEBUGING :
        print(*txt)
"""
#debug=print

#debug("salut")

#debug("salut","ca va")

def debug(*txt):
    if DEBUGING:
        print("[DEBUG]:",*txt)

def info(nom_fichier,*txt):
    """ne pas oublier de donner le nom du fichier dans le quelle la fonction est appeler"""
    if INFO:
        print("[INFO]["+nom_fichier+"]",*txt)

log=debug
