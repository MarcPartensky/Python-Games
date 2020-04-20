from collections import OrderedDict


class Map(OrderedDict):

    def set(self, m):
        self.clear()
        for [k, v] in m.items():
            self[k] = v

    def sort(self, f=lambda e: e):
        self.set(self.sorted(f))

    def sortKeys(self, f):
        self.set(self.sortedKeys(f))

    def sortValues(self, f):
        self.set(self.sortedValues(f))

    def sorted(self, f=lambda e: e):
        return Map(sorted(self.items(), key=f))

    def sortedKeys(self, f=lambda e: e[0]):
        return Map(sorted(self.items(), key=f))

    def sortedValues(self, f=lambda e: e[1]):
        return Map(sorted(self.items(), key=f))

    def forEach(self, f): #Not a fan
        for e in self.values():
            e=f(e)


if __name__ == "__main__":
    d = {1: 5, 3: 4, 0: 3}
    print(list(sorted(d)))
    m = Map(d)
    print(m)
    print(m.values())
    print(m.keys())
    print(len(m))
    print(next(m))
    print(next(m))
    print(next(m))
    print(m)
    m.sort()
    print(m.sortedValues())
    print(m.sortedKeys())
    print(list(iter(m)))

    for (k, e) in m.items():
        print(k, e)
