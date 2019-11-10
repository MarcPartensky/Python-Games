from myabstract import Segment
from mycontext import Context


segs=[Segment.random() for i in range(10)]

context=Context()
while context:
    context.check()
    context.control()
    context.clear()
    context.show()

    for seg in segs:
        seg.show(context)

    context.flip()
