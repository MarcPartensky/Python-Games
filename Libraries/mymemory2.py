import shelve

def save(object,filename):
    """Save all objects using filename."""
    #if filename[-5:]!=".shelve":
    #    filename+=".shelve"
    #saved=shelve.dumps(object)
    with open(filename,"w") as file:
        shelve.dump(object,file)


def load(object,filename):
    """Load object using filename."""
    #if filename[-5:]!=".shelve":
    #    filename+=".shelve"
    with open(filename,"r") as file:
        object=shelve.loads(loaded)
    return object
