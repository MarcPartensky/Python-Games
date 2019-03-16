import inspect


def test(arg1,arg2):
    a = arg1 + arg2
    return a

    #do something with args

keywords=["assert","break","class","continue","def","del","elif","else","except","finally","for",
          "from","global","if","import","in","pass","print","raise","return","try","while","yield"]

conversion1 = {"assert":"ASSERT",
              "break":"SORTIR DE LA BOUCLE",
              "class":"CLASSE",
              "continue":"CONTINER",
              "def":"DONNEES",
              "del":"SUPPRIMER",
              "elif":["SINON SI","FAIRE"],
              "else":["SINON","FAIRE"],
              "except":"EXCEPTE",
              "finally":"FINALLEMENT",
              "for":["POUR","FAIRE"],
              "from":"DEPUIS",
              "global":"GLOBAL",
              "if":"SI",
              "import":"IMPORTER",
              "in":"DANS",
              "pass":"PASSER",
              "print":"AFFICHER",
              "raise":"RELEVER",
              "return":"AFFICHER",
              "try":"ESSAYER",
              "while":["TANT QUE","FAIRE"],
              "yield":"PASSER AU TOUR SUIVANT",
              "==":"=",
              "=":"<-"}



def algorithm(name):
    lines = inspect.getsource(name)
    output = []
    lines = lines.split("\n")
    for line in lines:
        output.append(Converter(line)())
        #print("output: ",output)
    return "\n".join(output)


class Converter:
    def __init__(self,line):
        self.line=line
        self.alphabet="abcdefghijklmnopqrstuvwxyz"
        self.numbers="0123456789"
        self.punctuation="():.,"
        self.conversion= {"assert":     [[None,"assert",None],              [None,"ASSERT",None]],
                          "break":      [[None,"break"],                    [None,"SORTIR DE LA BOUCLE"]],
                          "class":      [["class",None],                    ["CLASS",None]],
                          "continue":   [[None,"continue",None],            [None,"CONTINUER",None]],
                          "def":        [["def",None,"(",None,"):"],        [None,":\nDONNES: ",None," :"]],
                          "del":        [[None,"del",None],                 [None,"SUPPRIMER",None]],
                          "elif":       [[None,"elif",None,":"],            [None,"SINON SI",None," FAIRE"]],
                          "else":       [[None,"else:",None],               [None,"SINON",None," FAIRE"]],
                          "except":     [[None,"except:",None],             [None,"EXCEPTE",None]],
                          "finally":    [[None,"finally:",None],            [None,"FINALLEMENT",None]],
                          "for":        [["for",None," in ",None,":"],      ["POUR",None," DANS ",None," FAIRE"]],
                          "from":       [["from",None],                     ["DEPUIS",None]],
                          "global":     [["global",None],                   ["GLOBAL",None]],
                          "if":         [[None,"if ",None],                 [None,"SI",None]],
                          "import":     [[None,"import",None],              [None,"IMPORTER",None]],
                          " in ":       [[None," in ",None],                [None, "DANS ",None]],
                          " is ":       [[None," is ",None],                [None," EST ",None]],
                          "pass":       [[None,"pass"],                     [None,"PASSER",None]],
                          "print":      [[None,"print",None,"(",None,")"],  [None,"AFFICHER: ",None,None]],
                          "raise":      [[None,"raise",None],               [None,"RELEVER",None]],
                          "return":     [[None,"return",None],              [None,"AFFICHER",None]],
                          "try":        [[None,"try:",None],                [None,"ESSAYER",None]],
                          "while":      [["while ",None,":"],               ["TANT QUE ",None," FAIRE"]],
                          "yield":      [[None,"yield"],                    [None,"PASSER AU TOUR SUIVANT"]],
                          "==":         [[None,"==",None],                  [None,"=",None]],
                          "!=":         [[None,"!=",None],                  [None,"≠",None]],
                          "=":          [[None,"=",None],                   [None,"<=",None]],
                          "append":     [[None,".append(",None,")"],             ["AJOUTER A ",None," LA VALEUR ",None]]}

        self.removeIndent()


    def removeIndent(self):
        self.indent=0
        if self.line!="":
            while self.line[0]==" ":
                self.indent+=1
                self.line=self.line[1:]

    def convert(self):
        if not ("#" in self.line):
            for key in self.conversion:
                if key in self.line:
                    self.apply(key)

    def apply(self,key):
        #print("key:",key)
        l=self.missing(self.conversion[key][0])
        #print("l:",l)
        filled=self.fill(self.conversion[key][1],l)
        #print("filled:",filled)
        self.line="".join(filled)
        #print(self.line)

    def missing(self,l):
        """
        l=          ["def ",None,"(",None,"):"]
        self.line=  "def algorithm(name):"
        l1=["def","(","):"]
        """
        line=[]
        if l[0]==None:
            i=self.next(self.line,l[1])
            line.append(self.line[:i])
        for i in range(1,len(l)-1):
            #print("missing loop:",l[i-1],l[i],l[i+1])
            if l[i]==None:
                a=self.between(self.line,l[i-1],l[i+1])
                line.append(a)
                #print("a",a)
        if l[-1]==None:
            i=self.next(self.line,l[-2])+len(l[-2])
            line.append(self.line[i:])
        return line

    def removeNone(self,l):
        l1=[]
        for word in l:
            if word!=None:
                l1.append(word)
        return l1

    def between(self,text,word1,word2):
        i1=self.next(text,word1)+len(word1)
        i2=i1+self.next(text[i1:],word2)
        return text[i1:i2]

    def cut(self,text,word):
        for i in range(len(text)-len(word)+1):
            if text[i:i+len(word)]==word:
                break
        return [text[:i],word,text[i+len(word):]]

    def next(self,text,word):
        for i in range(len(text)-len(word)+1):
            if text[i:i+len(word)]==word:
                break
        return i

    def fill(self,l1,l2):
        line=[]
        for e1 in l1:
            if e1==None:
                line.append(l2[0])
                del l2[0]
            else:
                line.append(e1)
        return line

    def __call__(self):
        self.convert()
        return " "*self.indent+self.line



print(algorithm(algorithm))

#c=Converter("def test(arg1,arg2):")

#print(c.between("def test(arg1,arg2):","(",")"))
