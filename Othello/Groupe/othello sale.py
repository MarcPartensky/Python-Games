grille=[[0 for x in range(8)] for y in range(8)]
avantage=[[0 for x in range(8)] for y in range(8)]
grille[3][4]=1
grille[3][3]=2
grille[4][3]=1
grille[4][4]=2

def main():
    joueur=0
    for i in range(60):
        print("Entrer position")
        print("Joueur:",joueur+1)
        x=int(input("x: "))
        y=int(input("y: "))
        print("")
        print(grille)
        print("")
        grille[y][x]=joueur+1
        joueur=joueur%2+1

def getLines(grille,joueur):
    pass


def getLine(line,joueur,indent=0):
    nombre=0
    l=len(line)
    if l>2:
        print("level:",indent)
        nombre+=getLine(line[:-1],joueur,indent+1)
        nombre+=getLine(line[1:],joueur,indent+1)
        return nombre
    else:
        print(line)
        if line[0]==line[1]==joueur:
            return nombre+1
        else:
            return 0


ligne=[0,0,1,0,0,0,1,1]
print(getLine(ligne,0))
