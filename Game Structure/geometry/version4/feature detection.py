import cv2
import numpy as np
import matplotlib.pyplot as plt

sj="saint jalm.jpg"
vl="valentin.png"
tm="tetedemarc.png"
pm="profiledemarc.jpg"

def canny(image):
    #gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #blur=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(image,50,150)
    return canny

def region_of_interest(image):
    height=image.shape[0]
    triangle=np.array([(200,height),(500,height),(200,height)])


def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            print(lines)


def searchPoints(canny_image):
    """Return the list of white points of a canny image."""
    l=[]
    height,width=image.shape[:2]
    for x in range(width):
        for y in range(height):
            if canny_image[y][x]:
                l.append((x,y))
    return l


def gradient(image,d=1):
    """Return the gradient image of the image."""
    height,width=image.shape[:2]
    #gradient_image=np.zeros((height-1,width-1))
    directions=[(dx,dy) for dx in range(-d,d+1) for dy in range(-d,d+1) if not(dx==dy==0)]
    for x in range(width):
        for y in range(height):
            gradient_image=sum([image[y][x] for (dx,dy) in directions])

            if canny_image[y][x]:
                l.append((x,y))
        return ls

def isWithin(image,x,y,d=1):
    """Determine if a position is within the (0,0) and (width-d,height-d)."""
    height,width=image.shape[:2]
    return 0<=x<width-d and 0<=y<height

def countNeighbours(image,x,y,d=1):
    """Count the neighbours of the pixel of position (x,y)."""
    return sum([image[y+dy][x+dx] for dx in range(-d,d+1) for dy in range(-d,d+1) if not(dx==dy==0)])

def listNeighbours(image,x,y,d=1):
    """List the neighbours of the pixel of position (x,y)."""
    return [(x+dx,y+dy) for dx in range(-d,d+1) for dy in range(-d,d+1) if not(dx==dy==0) if image[y+dy][x+dx]]



def findTraces(image):
    """Find all the traces of an image."""
    height,width=image.shape[:2]
    for x in range(width):
        for y in range(height):
            pass


def findTrace(image,x,y):
    """Find a trace of an image."""
    branches=[]
    branch=[(x,y)]
    while image[y][x]:
        ns=listNeighbours(image,x,y)
        if len(ns)==1:
            x,y=ns[0]
            branch.append(x,y)
        else:
            branches.append(branch)
        for n in ns:
            pass





image=cv2.imread(tm)
canny=canny(image)
treshold=100
#lines=cv2.HoughLinesP(image,2,np.pi/180,treshold,np.array([]),minLineLength=40,maxLineGap=5)
#line_image=display_lines(image,lines)
print(len(canny[0]))


pts=searchPoints(canny)
print(len(pts))





cv2.imshow("result",canny)
cv2.waitKey(0)
cv2.destroyAllWindows()

#plt.imshow(canny)
#plt.show()
