import random
import config
def intersection_(liste):#todo revoir
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

def est_superieur(l1, l2) :#doit supporter les coeff negatifs
    """"demander alex"""
    base=max(l1+l2)+1
    n1=sum(l1[i]*(base**(len(l1)-i-1)) for i in range(len(l1)))
    n2=sum(l2[i]*(base**(len(l2)-i-1)) for i in range(len(l2)))
    return n1>=n2

def ajouter_coeff_alea(l1,l2) :
    alea_coeff = [0, 1]
    random.shuffle(alea_coeff)
    l1.append(alea_coeff[0])
    l2.append(alea_coeff[1])

def liste_tuple_vers_liste_liste(liste_de_tuple) :
    return [list(elem) for elem in liste_de_tuple]
def liste_liste_vers_liste_tuple(liste_liste) :
    return [tuple(l) for l in liste_liste]

def deco_debug(fonction):
    def new_fct(*args, **kwargs) :
        config.debug("~{}({},{})".format(fonction.__name__, args, kwargs))
        result=fonction(*args, **kwargs)
        config.debug("$", result)
        return result
    return new_fct

def intersection(*args) :
    """fait intersection de liste
exemple :
    intersection([1,2,3],[2,3],[5,3,4])==[3]
    intersection([(1,2),(3,4)],[(1,2),(2,2)])==[(1,2)]
    """
    def intersection2(l1, l2):
        resultat = []
        for i in l1:
            if i in l2:
                resultat.append(i)
        #print("l1",l1)
        #print("l2",l2)
        #print("r:",resultat)
        return resultat
    #print("a:",args)
    if len(args)==1:
        return args[0]
    elif len(args)==2:
        return intersection2(args[0], args[1])
    return intersection(intersection2(args[0], args[1]), *args[2:])

#print(intersection([1,2,3],[2,3],[5,3,4]))
#print(intersection([(1,2),(3,4)],[(1,2),(2,2)]))