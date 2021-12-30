def findNearestVal(list,val):
        diffs = [abs(list_val - val) for list_val in list]
        min_diff = min(diffs)
        min_index = diffs.index(min_diff)
        return (min_index,list[min_index])
