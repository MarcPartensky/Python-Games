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
    print(lines)
    output = []
    lines = lines.split("\n")
    lines=removeUselessIndent(lines)
    lines=Converter(lines)
    for line in lines:
        output.append(Converter(line)())
        #print("output: ",output)
    return "\n".join(output)


class Converter:
    def __init__(self,name):
        self.name=name
        self.code=inspect.getsource(name)
        print(self.code)
        self.lines=self.code.split("\n")
        self.indent_historic=[]
        self.indent=0
        self.cleanCode()

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
                          "from":       [["from",None,"import",None],       ["DEPUIS",None,"IMPORTER",None]],
                          "global":     [["global",None],                   ["GLOBAL",None]],
                          "if":         [[None,"if",None],                  [None,"SI",None]],
                          "import":     [[None,"import",None],              [None,"IMPORTER",None]],
                          " in ":       [[None," in ",None],                [None, "DANS ",None]],
                          " is ":       [[None," is ",None],                [None," EST ",None]],
                          "lambda":     [[None,"lambda",None,":",None],     [None,":\nDONNEES: ",None," :\nRENVOIE",None]],
                          "pass":       [[None,"pass"],                     [None,"PASSER",None]],
                          "print":      [[None,"print",None,"(",None,")"],  [None,"AFFICHER: ",None,None]],
                          "raise":      [[None,"raise",None],               [None,"RELEVER",None]],
                          "return":     [[None,"return",None],              [None,"AFFICHER",None]],
                          "try":        [[None,"try:",None],                [None,"ESSAYER",None]],
                          "while":      [["while ",None,":"],               ["TANT QUE ",None," FAIRE"]],
                          "yield":      [[None,"yield"],                    [None,"PASSER AU TOUR SUIVANT"]],
                          "True":       [[None,"True",None],                [None,"VRAI",None]],
                          "False":      [[None,"False",None],                [None,"FAUX",None]],
                          "==":         [[None,"==",None],                  [None,"=",None]],
                          "!=":         [[None,"!=",None],                  [None,"≠",None]],
                          "=":          [[None,"=",None],                   [None," <- ",None]],
                          "append":     [[None,".append(",None,")"],        ["AJOUTER A ",None," LA VALEUR ",None]],
                          "not":        [[None,"not",None],                 [None,"NON",None]]}


    def cleanCode(self):
        self.cleanIndents()


    def cleanIndents(self):
        self.line=self.lines[0]
        count=self.countIndent(self.line)
        for i in range(len(self.lines)):
            self.lines[i]=self.lines[i][4*count:]

    def trackIndent(self,i):
        print(i)
        indent=self.countIndent(self.lines[i])
        if indent>len(self.indent_historic):
            self.addElementIndentHistoric(i)
        if indent<len(self.indent_historic):
            self.delElementIndentHistoric(i)
        print("i:",i)
        print("self.lines[i]:",self.lines[i])
        print("indent:",indent)
        print("historic:",self.indent_historic)
        print("")
        self.indent=indent
        self.removeIndent(i)

            #self.indent_historic.append()

    def addElementIndentHistoric(self,i):
        l={ " while ":" TANT QUE ",
            " for ":  " POUR ",
            " if ":   " SI "}
        for e in l:
            if e in self.lines[i]:
                self.indent_historic.append(l[e])
                print(self.lines[i])
                print(e)
                print(e in self.lines[i])

    def delElementIndentHistoric(self,i):
        print(len(self.lines))
        print(i+1)
        self.lines[i]+="\n"+" "*4*(self.countIndent(self.lines[i+1])+1)+"FIN "+self.indent_historic[-1]
        del self.indent_historic[-1]

    def countIndent(self,line):
        i=0
        for i in range(len(line)):
            if line[i]!=" ":
                break
        return int(i/4)

    def removeIndent(self,i):
        count=self.countIndent(self.lines[i])
        self.line=self.line[count*4:]

    def removeCommentaries(self):
        self.commentaries=""
        if "#" in self.line:
            i=self.next(self.line,"#")
            self.commentaries=self.line[i:]
            self.line=self.line[:i]
        if "\"\"\"" in self.line:
            i=self.next(self.line,"\"\"\"")
            self.commentaries=self.line[i:]
            self.line=self.line[:i]

    def convert(self):
        breaking=False
        for key in self.conversion:
            if key=="==":
                breaking=True
            if key in self.line:
                self.apply(key)
                if breaking:
                    break

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

    def assemble(self):
        pass

    def __call__(self):
        for i in range(len(self.lines)):
            if i<len(self.lines)-1:
                self.trackIndent(i)
            self.indent=self.countIndent(self.lines[i])
            self.line=self.lines[i]
            self.removeCommentaries()
            self.convert()
            self.lines[i]= " "*4*self.indent+self.line+" "+self.commentaries
        self.cleanCode()

        l1,l2=self.lines[0].split("\n")
        l1="ALGORITHME: "+l1.upper() +"\n\n"
        self.lines[0]=l1+l2
        return "\n".join(self.lines)

if __name__=="__main__":
    print(Converter(test)())
    #c=Converter("def test(arg1,arg2):")
    #print(c.between("def test(arg1,arg2):","(",")"))
