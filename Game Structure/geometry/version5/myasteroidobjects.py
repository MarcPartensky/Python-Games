class PerlinAsteroid:
    def __init__(self):
        """Object of perlin asteroid:"""
        self.precision = 100
        self.color = mycolors.WHITE
        self.noise_max = 2
        self.phase = 0
        self.phase_dt = 0.01
        self.wo = 2 * math.pi
        self.form = self.getForm()

    def update(self):
        """Update the perlin asteroid."""
        self.form=self.getForm()
        self.phase += self.phase_dt

    def show(self,context):
        """Show the form."""
        self.form.show(context)

    def getPoints(self):
        """Return the points of the perlin asteroid."""
        points = []
        wo = self.wo
        nm = self.noise_max
        off = self.phase
        for i in range(self.precision):
            a = i / self.precision * wo
            xoff = nm * (math.cos(a + off) + 1) / 2
            yoff = nm * (math.sin(a + off) + 1) / 2
            r = noise.pnoise2(xoff + off, yoff + off)
            r = (r + 1) / 2
            x = r * math.cos(a)
            y = r * math.sin(a)
            points.append((x, y))
        return points

    def getForm(self):
        """Return the form of the perlin asteroid."""
        return Form.createFromTuples(self.getPoints(),color=self.color)

    def log(self,context):
        """Allow an easy debug of the asteroid."""
        text=[
        "Asteroid:log:",
        "precision:"+str(self.precision),
        "phase:"+str(self.phase),
        "color:"+str(self.color),
        "phase_dt:"+str(self.phase_dt),
        "wo:"+str(self.wo)
        ]
        context.console.appendLines(text)


class PerlinAsteroidBody(PerlinAsteroid):
    """This is a perlin asteroid with a body."""



if __name__=="__main__":
    from mycontext import Context
    pa=PerlinAsteroid()
