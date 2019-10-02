import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
#%matplotlib inline

settings=[-2.0,0.5,-1.25,1.25,3,3,80]

def mandelbrot(z,maxiter):
    c = z
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return maxiter

def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (r1,r2,[mandelbrot(complex(r, i),maxiter) for r in r1 for i in r2])


def mandelbrot_image(xmin,xmax,ymin,ymax,width=3,height=3,maxiter=80,cmap='hot'):
    print("Initiating the mandelbrot image.")
    dpi = 72 #Zoom of the image
    img_width = dpi * width #Find the width of the image using the zoom and the width of the set
    img_height = dpi * height #Same operation for the height
    x,y,z = mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter) #Find the set
    print("The set is done.")
    print(type(z[0]))

    fig, ax = plt.subplots(figsize=(width, height),dpi=72) #get plt components
    ticks = np.arange(0,img_width,3*dpi) #find the steps
    x_ticks = xmin + (xmax-xmin)*ticks/img_width #split the x axis
    plt.xticks(ticks, x_ticks)
    y_ticks = ymin + (ymax-ymin)*ticks/img_width #split the y axis
    plt.yticks(ticks, y_ticks)
    print("Image settings are done.")

    norm = colors.PowerNorm(0.3) #Cool colors i guess
    ax.imshow(z,cmap=cmap,origin='lower',norm=norm) #create a dope heat map
    print("Image is done.")


mandelbrot_image(-2.0,0.5,-1.25,1.25,maxiter=80,cmap='gnuplot2')
#img=Image.fromarray(ms,'RGB')
#img.show()
