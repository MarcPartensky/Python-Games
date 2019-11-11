# Python-Games

# Dependencies
- pygame (For displaying the game and detect the events)
- opencv (For recording video or screen)
- numpy (Useful in some cases of optimization)

# Introduction
This is where i post all my games made in python using pygame. Most of them are based on a self-made hierarchy to reinforce the abstraction and so-doing the efficiency of writing code.

# Hierarchy (composition)
- Manager
  - Context
    - Draw
      - Plane
      - Window
     - Console
     - Camera

The window is a layer of abstraction built on top of pygame in order to make it easier to use pygame when the syntax is too long of uneasy to use. In practice it is used in all programs and allow to create a working window in 1 line which can be shown and used easily.

The plane is responsible for going from a system of coordinates to another. In practice it is a way to have geometry components in a 'plane system' which makes it easier to use, and convert them into the system of coordinates of the window to show them.

The draw class is responsible for drawing basic geometrical shapes in screen's coordinates. Every time a new shape is being drawn, the draw class uses its plane object to convert the coordinates from the 'plane system' to the 'window system' and then uses its window object to show it.

The console is a way to show written informations about the program during the execution, it allows the user to debug using only 1 line directly on the screen. It can also be used to type directly into it using the keyboard during the execution thanks to the manager.

The camera has 3 main responsibilites
- it can directly display the record of a video made with the camera of the computer
- it can record this video and save it onto an mp4 format (or other formats)
- it can record the video of the screen and save it onto an mp4 format aswell.

The context is responsible for every graphical and visual tasks, it uses its draw object to draw geometrical shapes, its console to display informations, and its camera to record videos. In a way it is a class that does nothing except relaying tasks to the right objects. It gives the user a 'facade' that makes it easier to use all of this environment.

The manager allows the user to "control" the program. Most projects have main classes that unherit from this class.
It deals with the main loop, it has an update, show and react method that can be overrided to create main classes fast.


# Geometrical components

myabstract.py: Main geometrical shapes
- Point
- Direction
- Segment
- Vector
- Line
- Halfline
- Form
- Circle

myrect.py: Caracterize every rectangle and offers functions to use them (inspired from pygame)
- Rect

myrectangle.py: Geometrical rectangle that can be shown that unherits from Rect
- Rectangle

mycase.py: Geometrical case that can be shown
- Case

mypixel.py: Showable pixel that can be put in a 2d array, mainly used to draw maps
- Pixel

mycurves.py: All curves
- Trajectory
- BezierCurve

mypolynomials.py: Polynomial class
- Polynomial

mywidgets.py: Useful widgets to interact with the program visually
- Widget
- Button
- Slider

mycolors.py: Gives name to rgb colors and function to use them

mygrapher.py: Show any function like matplotlib would do but using the environment

mycomplexforms.py: Classes for more advanced forms

myzone.py: Class for a limited plane (because the plane is infinite)

mygraph.py: Create a graphical graph, that could be used in the future.

myinterpolation.py: Make polynomial or bezier interpolations of points using mathematics formulaes.


# Physical components

myforce.py: Caracterize a force and directly unherits from Vector
- Force

mymotion.py: Caracterizes every possible object motion using vectors for position, velocity and acceleration and more
- Motion
- Moment

mymaterial.py: Offers lots of properties to use position, velocity and acceleration easily
- Material

myphysics.py: Offers even more abstraction to use motion components easily and unherits from Material
- Physics

mybody.py: Class for any object that can move unherits from Physics or Material
- Body
- FrictionBody
- MaterialBody

myentity.py: Class for every living body
- Entity

myentitygroup.py: Deal with groups of entity, useful for collision detection
- EntityGroup

myanatomies.py: Create anatomies for any geometrical objects
- TrajectoryAnatomy


Deprecated:
- mymaterialpoint: point that can move
- mymaterialline: line that can move
- mymaterialsegment: segment that can move
- mymaterialform: form that can move and is made from material points
- mymaterialformcollider: detect collisions between material forms


# Interconnected Tools

myconnection.py: Uses socket, select and pickle module to communicate between servers and clients computers.
- Client
- Server


# Few projects description

- mysierpinski.py
  Draw a sierpinski triangle from random points.
  
- myfouriervf.py
  Uses the fourier transform to draw 2d shapes by computing the coefficients of fourier and using these.
  
- mygameoflife.py
  The game of life in 2d.
  
 - mymaze.py
  Resolves any given maze and offers a visualization while doing so.
  
 - myflockingsimulation.py
  Group simulation of boids.
  
 - myquadtree.py
  Quadtree to encompass points in trees, useful for collision detection
  
 - mysolarsystem.py
  Visualization of the solar system with astres which obbey true physical laws and move accordingly to reality.
  
 - mymandelbrot.py
  Visualization of the mandelbrot set and allow the user to zoom in until max float precision is reached (for now).
  
 - myraycasting.py
  Create rays that can be shown and stop when hitting walls.
  
 - myparticles.py
  Create physical particles that can interact according to physical laws.
  
 - mypainter.py (Deprecated)
  Allows the user to draw shapes and images easily.
  
 - mymenu.py (Deprecated, replaced by widget project)
  Graphical components for making game menus: buttons, pages, menus
  
 - myeconomicmenu.py (Made to replace mymenu.py but also deprecated and replaced by widget project)
   Graphical components for making game menus with less computation: buttons, pages, menus
   
 - myspaceship.py
  File for all space related classes: missiles, spaceships, triangle spaceships, spaceships groups, ...
  
 
 

  
  


