from mywindow import *

class ListDisplayer:
    def __init__(self,list,window,background_color=(0,0,0),line_color=(255,255,255),box_color=(0,0,0)):
        self.list=list
        self.window=window
        self.background_color=background_color
        self.box_color=box_color
        self.line_color=line_color
        self.printing_data=[[0]]

    def process1(self,element,indent=0,max_indent=0):
        if type(element) is list:
            indent+=1
            if indent>max_indent:
                max_indent=indent
            element=list
            l=len(list)
            self.printing_data.append([])
            for i in range(l):
                self.process1(element,indent,max_indent)
                #self.printing_data[i]=

        else:
            return

    def draw(self,coordonnates,color):
        x,y,sx,sy=coordonnates
        pygame.draw.line(self.window.screen, color, (x,y), (x+sx,y), 1)
        pygame.draw.line(self.window.screen, color, (x+sx,y), (x+sx,y+sy), 1)
        pygame.draw.line(self.window.screen, color, (x+sx,y+sy), (x,y+sy), 1)
        pygame.draw.line(self.window.screen, color, (x,y+sy), (x,y), 1)

    def drawAll(self,data):
        self.window.screen.fill(self.background_color)
        wsx,wsy=self.window.size

        ly=len(data)
        sy=int(wsy/ly/2)
        positions=[0]

        for y_ in range(ly):
            line=data[y_]
            lx=len(line)
            y=int((0.25+y_)*wsy/ly)
            sx=int(wsx/lx/2)

            for x_ in range(lx):
                box=line[x_]
                x=int((0.25+x_)*wsx/lx)
                print(x)

                self.draw([x,y,sx,sy],self.box_color)
                self.draw([x+1,y+1,sx-1,sy-1],self.line_color)

        self.window.flip()
        self.wait()
        self.end()

    def wait(self):
        while self.window.open:
            self.window.check()

    def end(self):
        self.window.kill()


data=[[0],[0,0,0],[0,0,0,1,1,1,2],[0,1,1,1,2,2,2,3,3,3,3,4,5,6,6]]
#data=[[0],[3],[2,5,7]]

size=[700,700]
window=Window(None,size)

displayer=ListDisplayer(data,window)
displayer.drawAll(data)
