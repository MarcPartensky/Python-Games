import math

Premier=lambda k:len([j for j in range(2,k) if k%j==0])==0

#print([j for j in range(2,67) if 67%j==0])


#print(Premier(2**57885161-1))
#print(math.log(2**1000000000)/math.log(2))

#print(math.log(2**57885161-1)/math.log(10))

"""Exemple of the decorator pattern"""

class Fruit:
    def __init__(self,name):
        self.name=name
    def manger(self):
        print("On me mange rip.")
    def __repr__(self):
        return self.name

class Troll:
    def __init__(self,fruit):
        self.fruit=fruit
    manger=Fruit.manger
    def __repr__(self):
        return "en fait je suis un legume"


banane=Fruit("banane")
banane.manger()
print(banane)

print("")

fausse_banane=Troll(banane)
fausse_banane.manger()
print(fausse_banane)
