def intersection(liste):#todo revoir
    for i in range(len(liste)):
        liste[i]=tuple(liste[i])
    liste=list(frozenset(liste))
    for i in range(len(liste)):
        liste[i]=list(liste[i])
    return liste

def linearBijection(x,ensemble_entree,ensemble_sortie):
    """Renvoie la valeur de f(x) par la bijection de l'ensemble_entree et l'ensemble_sortie."""
    min1,max1=ensemble_entree
    min2,max2=ensemble_sortie
    return x/(max1-min1)*(max2-min2)+min2
