def maxVal(lapscatters, column, queryrange):
    retval = None
    for i in queryrange:
        if retval == None:
            retval = lapscatters[i][column]
            continue
        retval = max(retval, lapscatters[i][column])
    return retval

def minVal(lapscatters, column, queryrange):
    retval = None
    for i in queryrange:
        if retval == None:
            retval = lapscatters[i][column]
            continue
        retval = min(retval, lapscatters[i][column])
    return retval

def firstVal(lapscatters, column, queryrange):
    for i in queryrange:
        return lapscatters[i][column]

def lastVal(lapscatters, column, queryrange):
    lastindex = 0
    for i in queryrange:
        lastindex = i
    return lapscatters[lastindex][column]


def avgVal(lapscatters, column, queryrange):
    retval = 0.0
    for i in queryrange:
        retval += lapscatters[i][column]
    retval /= len(queryrange)
    return retval