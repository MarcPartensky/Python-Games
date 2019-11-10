from sympy import Symbol

R=Symbol("R")
C=Symbol("C")
w=Symbol("w")

Zc=1/(1j*C*w)
x=R*C*w
print(Zc)
Zab1=2*R+R**2/Zc
Zab2=2*Zc+Zc**2/(R/2)

print(Zab1,Zab2)

Zab=Zab1*Zab2/(Zab1+Zab2)

print(Zab)
