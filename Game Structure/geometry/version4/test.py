from mysurface import Surface
from myabstract import Form,Segment,Line
surface=Surface()

line=Line.random()
segment=Segment.random()
print(line|segment)

while surface.open:
    surface.check()
    surface.control()
    surface.clear()
    surface.show()

    line.show(surface)
    segment.show(surface)

    surface.flip()
