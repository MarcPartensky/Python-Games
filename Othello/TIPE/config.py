#CASES=[0,1]

CASE_VIDE=-1 #Ne pas mettre 0 ou 1
DEBUGING=True
import sys

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

log=debug
