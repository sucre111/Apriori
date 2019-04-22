import itertools
from collections import defaultdict

def candidateGen(itemSets, k):
    candidate = []

    if k == 2:
        candidate = [tuple(sorted([x[0], y[0]])) for x in itemSets for y in itemSets if len((x[0], y[0])) == k and x[0] != y[0]]
    else:
        candidate = [tuple(sorted(set(x).union(y))) for x in itemSets for y in itemSets if list(x)[0:-1] == list(y)[0:-1] and list(x)[-1] != list(y)[-1]]
    candidate = list(set(candidate))
    for c in candidate:
        subsets = genSubsets(c, k-1)
        if any([x not in itemSets for x in subsets]):
            candidate.remove(c)

    return set(candidate)

def candidateGen2(itemSets1, itemSets2, items1, items2, k):
    candidate = []
    candidate = [tuple(set(x).union([y])) for x in itemSets1 for y in items2 if itemSets1 != set([])] + [tuple(set(x).union([y])) for x in itemSets2 for y in items1 if itemSets2 != set([])]
    candidate = [x for x in candidate if len(x) == k]
    return set(candidate)



def genSubsets(items, m):
    subsets = []
    subsets.extend(itertools.combinations(items, m))
    return subsets


def countAndCate(C, ds, minSup, maxSup, freqDict):
    for trans in ds:
        for cand in C:
            if len(cand) > len(trans):
                continue
            if set(cand).issubset(trans):
                freqDict[cand] += 1
    freqSet = set()
    rareSet = set()
    # zeroSet = set()
    # fitems = set()
    # ritems = set()
    for cand in C:
        f = freqDict[cand]
        if f >= maxSup:
            freqSet.add(cand)
            # fitems = fitems.union(cand)
        elif f >= minSup:
            rareSet.add(cand)
            # ritems = ritems.union(cand)
    return freqSet, rareSet




def runApriori(ds, minSup, maxSup):
    freqDict = defaultdict(int)
    # itemSet = set()
    C = set()
    for trans in ds:
        for item in trans:
            # itemSet.add(item)
            C.add(tuple([item]))

    freqSet = set()
    rareSet = set()
    # zeroSet = set()

    # freqSet, rareSet, fitems, ritems = countAndCate(C, ds, minSup, maxSup, freqDict)
    freqSet, rareSet = countAndCate(C, ds, minSup, maxSup, freqDict)

    fitems = set([x[0] for x in freqSet])
    ritems = set([x[0] for x in rareSet])

    L = freqSet
    R = rareSet
    # L[1] = freqSet
    # R[1] = rareSet
    k = 2
    while(freqSet != set(()) or rareSet != set(())):
        C = set()
        LR = candidateGen2(freqSet, rareSet, fitems, ritems, k)
        C = C.union(LR)
        freqSet = candidateGen(freqSet, k)
        C = C.union(freqSet)
        rareSet = candidateGen(rareSet, k)
        C = C.union(rareSet)

        # freqSet, rareSet, fitems, ritems= countAndCate(C, ds, minSup, maxSup, freqDict)
        freqSet, rareSet = countAndCate(C, ds, minSup, maxSup, freqDict)

        L = L.union(freqSet)
        R = R.union(rareSet)
        k += 1

    LitemSets = dict()
    for s in L:
        LitemSets[frozenset(s)] = freqDict[s]
    RitemSets = dict()
    for s in R:
        RitemSets[frozenset(s)] = freqDict[s]

    return LitemSets, RitemSets

if __name__ == '__main__':
    ds = [(1, 2, 3), (2,), (1, 4), (1, 3, 4), (2,3),(4,5) ]
    L, R = runApriori(ds, 1, 3)
    print(L)
    print(R)
