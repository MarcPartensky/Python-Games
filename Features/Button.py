class Button:
    def __init__(self,content,action,colors=[BLACK,WHITE,BLACK]):
        self.content=content
        self.action=action
        self.colors=(self.text_color,self.background_color,self.border_color)=colors

    def set(self,position,size,border=3):
        self.position=position
        self.size=size
        self.border=b=border

    def show(self,window):
        x,y=self.position
        sx,sy=self.size
        (dtx,dty)=(5,3)
        pygame.draw.rect(window.screen, self.border_color, (x,y,sx,sy), 0)
        pygame.draw.rect(window.screen, self.background_color, (x+b,y+b,sx-2*b,sy-2*b), 0)
        label = self.window.font.render(self.content, 1, self.text_color)
        window.screen.blit(label, (x+dtx,y+dty))

    def check(self,position):
        kx,ky=position
        bx,by=self.position
        sx,sy=self.size
        if abs(kx-bx)<sx and abs(ky-by)<sy:
            return True
        else:
            return False
