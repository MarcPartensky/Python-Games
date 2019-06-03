import time

def timer(function):
    """Print the duration of a function making use of decorators."""
    def newFunction(*args,**kwargs):
        """Tested function."""
        ti=time.time()

        result=fonction(*args,**kwargs)
        tf=time.time()
        dt=tf-ti
        print("[TIMER]: "+str(fonction.__name__)+" took "+str(dt)+" seconds.")
        return result
    return newFunction
