#made in lovinsky

grille=[[" "," "," "],
        [" "," "," "],
        [" "," "," "]]

"X"
"O"
" "

fin=False
etat=0

while not fin:
    valeur=input("Jouer:")
    tour=etat%2
    etat=etat+1
