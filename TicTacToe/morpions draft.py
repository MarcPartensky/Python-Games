import random
import itertools
import numpy as np
import copy
import time


def emptyGrid():
    return np.zeros((3, 3), dtype=int)


def allGrids():
    def f(x): return np.reshape(x, (3, 3))
    t = itertools.product(range(-1, 2), repeat=9)
    return list(map(f, t))


def getWinners(g):  # Perfect way to find winners, but almost twice as slow
    return (isWinner(g, -1), isWinner(g, 1))


def isWinner(g, a):
    if g[0][0] == g[1][0] == g[2][0] == a:
        return True
    if g[0][1] == g[1][1] == g[2][1] == a:
        return True
    if g[0][2] == g[1][2] == g[2][2] == a:
        return True

    if g[0][0] == g[0][1] == g[0][2] == a:
        return True
    if g[1][0] == g[1][1] == g[1][2] == a:
        return True
    if g[2][0] == g[2][1] == g[2][2] == a:
        return True

    if g[0][0] == g[1][1] == g[2][2] == a:
        return True
    if g[0][2] == g[1][1] == g[2][0] == a:
        return True
    return False


def outcome(g):  # Imperfect, there might be 2 winners with a random grid, but in a game it never happens
    if g[0][0] == g[1][0] == g[2][0] and g[0][0] != 0:
        return g[0][0]
    if g[0][1] == g[1][1] == g[2][1] and g[0][1] != 0:
        return g[0][1]
    if g[0][2] == g[1][2] == g[2][2] and g[0][2] != 0:
        return g[0][2]

    if g[0][0] == g[0][1] == g[0][2] and g[0][0] != 0:
        return g[0][0]
    if g[1][0] == g[1][1] == g[1][2] and g[1][0] != 0:
        return g[1][0]
    if g[2][0] == g[2][1] == g[2][2] and g[2][0] != 0:
        return g[2][0]

    if g[0][0] == g[1][1] == g[2][2] and g[0][0] != 0:
        return g[0][0]
    if g[0][2] == g[1][1] == g[2][0] and g[0][2] != 0:
        return g[0][2]

    return 0


def randomGrid():
    return np.random.randint(-1, 2, (3, 3), dtype=int)


def getAllWinners(gs):
    return [(g, getWinners(g)) for g in gs]


def randomPlay(g, p):
    cs = getChoices(g)
    c = random.choice(cs)
    g[c[0]][c[1]] = p


def toList(a): return list(np.reshape(a, (1, 9))[0])


def toArray(l): return np.reshape(l, (3, 3))


def getChoices(g):
    return [(x, y) for x in range(3) for y in range(3) if g[x][y] == 0]

# move = (position (x,y),winner)
# Choose the best possible move


def choose(g, c, p):
    ng = copy.deepcopy(g)
    ng[c[0]][c[1]] = p
    return ng


def get(l, f):
    for e in l:
        if f(e):
            return e


def bestMove(g, p):  # Super Minimax specially adapted for morpions
    choices = getChoices(g)
    if len(choices) == 1:
        g = choose(g, choices[0], p)
        w = outcome(g)
        return (choices[0], w)
    else:
        moves = []
        for choice in choices:
            ng = choose(g, choice, p)
            w = outcome(ng)
            if w == p:  # We already won, so it's needless to compute further
                return (choice, w)
            else:
                moves.append(bestMove(ng, -p))
        if p == 1:
            m = max(moves, key=lambda x: x[1])
            return [choices[moves.index(m)], m[1]]
        else:
            m = min(moves, key=lambda x: x[1])
            return [choices[moves.index(m)], m[1]]


def bestMoveShort(g, p):  # Super Minimax specially adapted for morpions
    choices = getChoices(g)
    if len(choices) == 1:
        w = outcome(choose(g, choices[0], p))
        return (choices[0], w)
    else:
        moves = []
        for choice in choices:
            w = outcome(choose(g, choice, p))
            if w == p: return (choice, w) # We already won, so it's needless to compute further
            moves.append(bestMove(ng, -p))
        m = max(moves, key=lambda x: p*x[1]) #We use the fact that p equals 1 or -1
        return [choices[moves.index(m)], m[1]]

def bestMove2(g, p):  # Super Minimax specially adapted for morpions
    choices = getChoices(g)
    if len(choices) == 1:
        g = choose(g, choices[0], p)
        w = outcome(g)
        return [0, w]
    else:
        moves = []
        for i, choice in enumerate(choices):
            ng = choose(g, choice, p)
            w = outcome(ng)
            if w == p:  # We already won, so there is no need to compute further
                return (i, w)
            else:
                moves.append(bestMove2(ng, -p))
        if p == 1:
            m = max(moves, key=lambda x: x[1])
            return [moves.index(m), m[1]]
        else:
            m = min(moves, key=lambda x: x[1])
            return [moves.index(m), m[1]]


def bestPlay(g, p):
    m = bestMove(g, p)
    c = m[0]
    g[c[0]][c[1]] = p


def bestPlay2(g, p):
    cs = getChoices(g)
    i, w = bestMove2(g, p)
    print(i, w)
    c = cs[i]
    g[c[0]][c[1]] = p


def predictedPlay(g, p, i, choices=[(1, 2), (1, 1), (1, 0)]):
    c = choices[i // 2]
    g[c[0]][c[1]] = p


def player(i):  # return the player on the i-th turn
    return 2 * (i % 2) - 1


def main():
    g = emptyGrid()
    i = 0
    w = 0
    while w == 0 and toList(g).count(0) != 0:
        p = player(i)
        if i % 2 == 0:
            bestPlay2(g, p)
        else:
            #randomPlay(g, p)
            #predictedPlay(g, p, i)
            bestPlay(g, p)
        w = outcome(g)
        i += 1
        print(g, end='\n\n')
    print("the winner is:", w)


if __name__ == "__main__":
    to = time.time()
    main()
    print("Execution time:", time.time() - to)
