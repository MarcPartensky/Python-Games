def intersection(liste):#todo revoir
    for i in range(len(liste)):
        liste[i]=tuple(liste[i])
    liste=list(frozenset(liste))
    for i in range(len(liste)):
        liste[i]=list(liste[i])
    return liste
