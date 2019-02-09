import pickle

def save(object,filename):
    """Save all objects using filename."""
    #if filename[-5:]!=".pickle":
    #    filename+=".pickle"
    saved=pickle.dumps(object)
    with open(filename,"w") as file:
        pickle.dump(saved,file)


def load(object,filename):
    """Load object using filename."""
    #if filename[-5:]!=".pickle":
    #    filename+=".pickle"
    with open(filename,"r") as file:
        loaded=pickle.load(filename,file)
        object=pickles.loads(loaded)
    return object
