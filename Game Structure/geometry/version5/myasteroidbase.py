from myabstract import Form, Point, Circle
import mycolors
import math


class SpiderBaseAnatomy(Form):
    """Anatomy of a spider base."""

    def __init__(self, n=5, radius=10, rotation=0.001,
                 posts_radius=2, post_radius=3,
                 **kwargs):
        """Create a spider base using the number of posts."""
        self.posts_radius = posts_radius
        self.post_radius = post_radius
        self.rotation = rotation
        points = []
        for i in range(n):
            angle = 2 * math.pi * i / n
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append(Point(x, y))
        super().__init__(points, **kwargs)

    def show(self, context):
        super().show(context)
        for post in self.posts:
            post.show(context)
        self.post.show(context)

    def update(self, dt):
        self.rotate(self.rotation)

    @property
    def posts(self):
        """Return the front posts."""
        circles = []
        for p in self.points:
            circles.append(Circle(*p, radius=self.posts_radius, color=self.side_color,
                                  area_color=self.area_color, fill=self.fill))
        return circles

    @property
    def post(self):
        """Return the main post."""
        return Circle(0, 0, radius=self.post_radius, color=self.side_color,
                      area_color=self.area_color, fill=self.fill)


if __name__ == "__main__":
    from mymanager import BodyManager

    station = SpiderBaseAnatomy(side_color=mycolors.RED)
    m = BodyManager(station, dt=0.1)
    m()
