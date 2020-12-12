import pandas as pd
import numpy as np

# Return : ("D", dfList)
# [df.name in dfList] = ["D_0", "D_1", ...]
# df.columns = {"C": ["C_0", "C_1", ...]}
# df.index = {"I": ["I_0", "I_1", ...]}
def makeDfList():
    numDf = 5  # number of df
    minN = 10  # min index count
    maxN = 20  # max index count
    # --- make dfList
    dfList = []
    for bmIdx in list(range(numDf)):
        numItem = np.random.randint(minN, maxN + 1)
        dictList = [{"Frame": val+1} for val in list(range(0, numItem + 1))]
        df = pd.DataFrame(dictList)
        df.rename_axis(index="I", columns="C", inplace=True)
        df.name = "D_{}".format(bmIdx)
        dfList += [df]
    retData = ("D", dfList)
    # --- update dfList
    for (idx, df) in enumerate(dfList):
        mean = np.random.randint(1, 5 + 1)
        sigma = np.random.randint(1, 1 + 1)
        offset = np.random.randint(0, 100 + 1)
        df["primitives"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixels"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixel1"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixel2"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel3"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel4"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel5"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel6"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel7"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel8"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel9"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel10"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        # df["pixel11"]  = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
    return retData

def makeDfG(listName, dfList, reduced):
    if reduced == "list":
        dfMVi = pd.concat(dfList, axis="index", join="inner", keys=[df.name for df in dfList])
        dfG = dfMVi.groupby(axis="index", level=1)
        # --- columns.name = "C"
        # --- index.name (level=0) = "I"
        # --- index.name (level=1) = "D"    --> to be reduced by group functions
    elif reduced == "index":
        dfMVo = pd.concat(dfList, axis="index", join="outer", names=[listName, dfList[0].index.name], keys=[df.name for df in dfList])
        dfG = dfMVo.groupby(axis="index", level=0)
        # dfG_CD.rename_axis(index=listName, inplace=True)
        # --- columns.name = "C"
        # --- index.name (level=0) = "D"
        # --- index.name (level=1) = "I"    --> to be reduced by group functions
    elif reduced == "columns":
        dfMHo = pd.concat(dfList, axis="columns", join="outer", names=[listName, dfList[0].columns.name], keys=[df.name for df in dfList])
        dfMHo.index.name = dfList[0].index.name
        dfG = dfMHo.groupby(axis="columns", level=0)
        # --- columns.name (level=0) = "D"
        # --- columns.name (level=1) = "C"  --> to be reduced by group functions
        # --- index.name = "I"
    else:
        assert False, "not supported option '{}' for the parameter of 'reduced'".format(reduced)
    return dfG

# ====================================================================================================
# Private
# ====================================================================================================

def _testDfGroupPrint(dfG):
    print ("===== Sum ========================================")
    dfCntSum = dfG.sum()
    print (dfCntSum)
    print ("===== Mean =======================================")
    dfCntMean = dfG.mean()
    print (dfCntMean)
    print ("===== CntSum/Col0Sum==============================")
    dfCntSumCol0 = dfCntSum.divide(dfCntSum[dfCntSum.columns[0]], axis="index")
    print (dfCntSumCol0)

def _testDfGroup(listName, dfList):
    print ("================================================================================")
    dfG = makeDfG(listName, dfList, "list")
    _testDfGroupPrint(dfG)
    print ("================================================================================")
    dfG = makeDfG(listName, dfList, "index")
    _testDfGroupPrint(dfG)
    print ("================================================================================")
    dfG = makeDfG(listName, dfList, "columns")
    _testDfGroupPrint(dfG)
    print ("================================================================================")

if __name__ == "__main__":
    (listName, dfList) = makeDfList()
    # --- [df.name in dfList] = ["D_0", "D_1", ...]
    # --- df.columns.name = "C"
    # --- df.index.name = "I"
    print ("####################################################################################################")
    _testDfGroup(listName, dfList)
    print ("####################################################################################################")

    # _testDfLoop(dfMH)