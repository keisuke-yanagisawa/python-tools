# coding: UTF-8 

import pandas as pd
import math
def ef(values, labels, ratio, definition=(0,1)):
    """
    INPUT
    values     : value list for sorting (descending order is assumed)
    labels     : label list for evaluation
    ratio      : a ratio of EF that you want to calculate
    definition : definition of positive and negative labels (default=(0,1), 0 for neg, 1 for pos)

    OUTPUT
    an enrichment factor (ratio)
    """

    if len([x for x in labels if (not x in definition)]) != 0:
        print("invalid labels are detected.")
        print([x for x in labels if (not x in definition)])
        return None
    if ratio > 1:
        print("ratio %f is invalid. ratio must be no more than 1." % ratio)
        return None
    labels = [definition.index(x) for x in labels]
    ratio1 = float(sum(labels))/len(labels)
    df = pd.DataFrame.from_dict({"value": values, "label": labels}).sort_values("value", ascending=False).reset_index();
    labels = pd.merge(df[["value"]], df.groupby("value").mean().reset_index(), on="value", how="left").label

    index = len(labels)*ratio
    decimal, integer = math.modf(index)
    integer = int(integer)

    labelsN = labels[:integer]
    if decimal != 0:
        ratioN = ( float(sum(labelsN)) + labels[integer+1]*decimal ) / index
    else:
        ratioN = float(sum(labelsN)) / index
    ef = ratioN / ratio1;
    return ef

def test(cond, statement_dict):
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if cond:
        print(OKGREEN+"A test is passed."+ENDC)
    else:
        print(FAIL+"A test is failed."+ENDC)
    for key, value in statement_dict.iteritems():
        print(key, value)

if __name__ == '__main__':
    case1 = {
        "values": [1, 2, 3, 4, 5],
        "labels": [0, 0, 1, 0, 1],
        "ratio" : 0.2,
        "result": (1.0/1) / (2.0/5),
    }
    test(ef(case1["values"], case1["labels"], case1["ratio"]) == case1["result"], case1)


    case2 = {
        "values"     : [1, 2, 3, 4, 5],
        "labels"     : [0, 0, 1, 0, 1],
        "ratio"      : 0.2,
        "result"     : (0.0/1) / (2.0/5),
        "definition" : (1,0),
    }
    test(ef(case2["values"], case2["labels"], case2["ratio"], definition=case2["definition"]) == case2["result"], case2)

    case3 = {
        "values"     : [1, 2, 4, 4, 5],
        "labels"     : [0, 0, 1, 0, 1],
        "ratio"      : 0.4,
        "result"     : (1.5/2) / (2.0/5),
    }
    test(ef(case3["values"], case3["labels"], case3["ratio"]) == case3["result"], case3)
    

    case4 = {
        "values"     : [1, 2, 4, 4, 5],
        "labels"     : [0, 0, 1, 0, 1],
        "ratio"      : 0.3,
        "result"     : (1.25/1.5) / (2.0/5),
    }
    test(ef(case4["values"], case4["labels"], case4["ratio"]) == case4["result"], case4)
    
    case4 = {
        "values"     : [1, 2, 4, 4, 5],
        "labels"     : [0, 0, 1, 0, 1],
        "ratio"      : 1.0,
        "result"     : (2.0/5) / (2.0/5),
    }
    test(ef(case4["values"], case4["labels"], case4["ratio"]) == case4["result"], case4)
