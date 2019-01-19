class Block:
    def __init__(self,grid):
        self.grid=grid
        self.size=[len(grid),len(grid[0])]
        
    def show(self,window,coordonates):
        cx,cy,csx,csy=coordonates
        sx,sy=self.size
        for y in range(sy):
            for x in range(sx):
                X=int(cx+csx*x/sx)
                Y=int(cy+csy*y/sy)
                SX=int(csx/sx)
                SY=int(csy/sy)
                raw_coordonnates=(X,Y,SX,SY)
                pygame.draw.rect(window.screen,self.grid[y][x],raw_coordonnates,0)
