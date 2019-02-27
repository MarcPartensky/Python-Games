from mywindow import Window
from mycolors import WHITE,BLACK

from Othello import Othello

window=Window(size=[800,800],set=False)
window.open=True
window.text_color=BLACK
window.background_color=BLACK
window.text_size=30
#window.size=[900,20]

results=[]
i=0
number=10000
display=False

while i<number and window.open:
    i+=1
    game=Othello(window,display)
    game()
    winner_side=(game.state+1)%2
    results.append(winner_side)
    message="Results for "+str(i)+" tests:\n"+"White victories: "+str(results.count(0))+"\n"+"Black victories: "+str(results.count(1))+"\n"
    window.print(str(message),size=[50,20])
    window.flip()
    print(message)




message="Results for "+str(i)+" tests:\n"+"White victories: "+str(results.count(0))+"\n"+"Black victories: "+str(results.count(1))+"\n"
print(message)
