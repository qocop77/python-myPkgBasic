import pandas as pd
import numpy as np

# --- The axis to be reduced is set to level=1 index in 2-level multi-indexes
def makeDfM(listName, dfList, reduce):
    if reduce == "index":
        dfM = pd.concat(dfList, axis="index", keys=[df.name for df in dfList], names=[listName, dfList[0].index.name])
            # --- columns.name = "C"
            # --- index.name (level=0) = "L"
            # --- index.name (level=1) = "I"    <-- to be reduced
    elif reduce == "list":
        dfM = pd.concat(dfList, axis="index", keys=[df.name for df in dfList], names=[listName, dfList[0].index.name])
        dfM = dfM.swaplevel(0, 1, axis="index")
            # --- columns.name = "C"
            # --- index.name (level=0) = "I"
            # --- index.name (level=1) = "L"    <-- to be reduced
    elif reduce == "columns":
        # --- 1) change C and L in dfList
        dfM = pd.concat(dfList, axis="columns", keys=[df.name for df in dfList], names=[listName, dfList[0].columns.name])
            # --- columns.name (level=0) = "D"
            # --- columns.name (level=1) = "C"
            # --- index.name = "I"
        dfNewList = []
        for col in dfList[0].columns:
            dfNew =  dfM.xs(col, level=1, axis="columns")
            dfNew.name = col
            dfNew.index.name = dfList[0].index.name
            dfNew.columns.name = listName
            dfNewList += [dfNew]
        listName = dfList[0].columns.name
        dfList = dfNewList
        # --- 2) handle it like the above "list" case
        dfM = pd.concat(dfList, axis="index", keys=[df.name for df in dfList], names=[listName, dfList[0].index.name])
        dfM = dfM.swaplevel(0, 1, axis="index")
            # --- columns.name = "L"
            # --- index.name (level=0) = "I"
            # --- index.name (level=1) = "C"    <-- to be reduced
    else:
        assert False, "not supported option '{}' for the parameter of 'reduce'".format(reduce)
    return dfM

# --- make dfList for test
# --- Return : ("L", dfList), where
# --- --- [df.name in dfList] = ["D_0", "D_1", ...]
# --- --- df.columns = {"C": ["C_0", "C_1", ...]}
# --- --- df.index = {"I": ["I_0", "I_1", ...]}
def makeTestDfList():
    numDf = 7  # ---number of df
    minN = 10  # ---min index count
    maxN = 20  # ---max index count
    # --- make dfList
    dfList = []
    for bmIdx in list(range(numDf)):
        numItem = np.random.randint(minN, maxN + 1)
        dictList = [{"Frame": val+1} for val in list(range(0, numItem + 1))]
        df = pd.DataFrame(dictList)
        df.rename_axis(index="I", columns="C", inplace=True)
        df.name = "L_{}".format(bmIdx)
        dfList += [df]
    retData = ("L", dfList)
    # --- update dfList
    for (idx, df) in enumerate(dfList):
        mean = np.random.randint(1, 5 + 1)
        sigma = np.random.randint(1, 1 + 1)
        offset = np.random.randint(0, 100 + 1)
        df["primitives"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixel1"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixel2"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
        df["pixel3"] = np.random.normal(mean, sigma, size=len(df)) * 100 + offset
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

# ====================================================================================================
# Private
# ====================================================================================================

def _testDfGroupPrint(dfM):
    dfG = dfM.groupby(axis="index", level=0)
    print ("===== Sum ========================================")
    dfCntSum = dfG.sum()
    print (dfCntSum)
    # print ("===== Mean =======================================")
    # dfCntMean = dfG.mean()
    # print (dfCntMean)
    # print ("===== CntSum/Col0Sum==============================")
    # dfCntSumCol0 = dfCntSum.divide(dfCntSum[dfCntSum.columns[0]], axis="index")
    # print (dfCntSumCol0)

def _testDfGroup(listName, dfList):
    print ("\n===== ( reduce = index ) =======================================================")
    dfM = makeDfM(listName, dfList, "index")
    _testDfGroupPrint(dfM)
    print ("\n===== ( reduce = list ) ========================================================")
    dfM = makeDfM(listName, dfList, "list")
    _testDfGroupPrint(dfM)
    print ("\n===== ( reduce = columns ) =====================================================")
    dfM = makeDfM(listName, dfList, "columns")
    _testDfGroupPrint(dfM)

def _testDfLoopPrint(dfM):
    dfG = dfM.groupby(axis="index", level=1)
    for (name, df) in dfG:
        df = df.droplevel(axis="index", level=1)
        print ("===== ( name = {} ) ============================================================".format(name))
        print (df)

def _testDfLoop(listName, dfList):
    # --- NOTE : The below (reduce=index) case shows too many dataFrames for all index values
    # print ("===== ( reduce = index ) =======================================================")
    # dfM = makeDfM(listName, dfList, "index")
    # _testDfLoopPrint(dfM)
    print ("\n===== ( reduce = list ) ========================================================")
    dfM = makeDfM(listName, dfList, "list")
    _testDfLoopPrint(dfM)
    print ("\n===== ( reduce = columns ) =====================================================")
    dfM = makeDfM(listName, dfList, "columns")
    _testDfLoopPrint(dfM)

if __name__ == "__main__":
    (listName, dfList) = makeTestDfList()
    # --- [df.name in dfList] = ["D_0", "D_1", ...]
    # --- df.columns.name = "C"
    # --- df.index.name = "I"
    print ("\n\n##### Group Test ###################################################################################")
    _testDfGroup(listName, dfList)
    print ("\n\n##### Loop Test ####################################################################################")
    _testDfLoop(listName, dfList)
    print ("\n\n####################################################################################################")