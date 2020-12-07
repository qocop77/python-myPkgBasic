import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
import myPkgBasic.os as myOs

def annotateBoxplot(bpdict, ax, pctStrList, pctHideStrList, x_offset=0.05, x_loc=0, annotate_params=None):
    if annotate_params is None:
        annotate_params = dict(xytext=(15, 10), textcoords='offset points', arrowprops={'arrowstyle':'->'})
    valList  = []
    valList += [bpdict['means'][x_loc].get_ydata()[0]]
    valList += [bpdict['caps'][x_loc*2].get_ydata()[0]]
    valList += [bpdict['boxes'][x_loc].get_ydata()[0]]
    valList += [bpdict['medians'][x_loc].get_ydata()[0]]
    valList += [bpdict['boxes'][x_loc].get_ydata()[2]]
    valList += [bpdict['caps'][(x_loc*2)+1].get_ydata()[0]]
    for (idx, _) in enumerate(pctStrList[6:]):
        valList += [bpdict['fliers'][x_loc].get_ydata()[idx]]
    for (idx, pctStr) in enumerate(pctStrList):
        if not pctStr in pctHideStrList:
            ax.annotate(
                "{} : {}".format(pctStr, np.round(valList[idx], 2))
                , (x_loc + 1 + x_offset, valList[idx])
                , **annotate_params
            )

def drawSubBoxplot (df, ax, pctAddList=[], pctHideStrList=[]):
    pctDefList = [0, 25, 50, 75, 100]
    pctDefStrList = ["mean"] + [str(pct)+"%" for pct in pctDefList]
    # --- original boxplot : fixed percentile of 0%, 25%, 50%, 75%, 100%
    # bpdict = df.boxplot(ax=ax
    #     , return_type='dict'
    #     , whis="range"
    #     , column=df.columns.to_list()
    #     , showmeans=True
    #     , notch=False
    #     , fontsize=7
    #     , flierprops=dict(markerfacecolor='r', marker='s')
    # )
    # pctStrList = pctDefStrList
    # for (serIdx, _) in enumerate(df):
    #     annotateBoxplot(bpdict, ax, pctStrList, pctHideStrList, x_loc=serIdx)
    # --- customized boxplot
    pctAddStrList = [str(pctAdd)+"%" for pctAdd in pctAddList]
    dfStats = df.describe(percentiles=[float(x)/100 for x in (pctDefList + pctAddList)])
    boxes = []
    for dfName in dfStats:
        boxes += [dict
            ( label= "{} (N={})".format(dfName, int(dfStats[dfName].loc["count"]))
            , whis="range"
            , mean=dfStats[dfName].loc[pctDefStrList[0]]
            , whislo= dfStats[dfName].loc[pctDefStrList[1]]
            , q1= dfStats[dfName].loc[pctDefStrList[2]]
            , med= dfStats[dfName].loc[pctDefStrList[3]]
            , q3= dfStats[dfName].loc[pctDefStrList[4]]
            , whishi= dfStats[dfName].loc[pctDefStrList[5]]
            , fliers= dfStats[dfName].loc[pctAddStrList]
            , flierprops=dict(markerfacecolor='r', marker='s')
            , fontsize=7
            )
        ]
    bpdict = ax.bxp(boxes, showmeans=True, showfliers=True)
    pctStrList = pctDefStrList + pctAddStrList
    for (serIdx, _) in enumerate(df):
        annotateBoxplot(bpdict, ax, pctStrList, pctHideStrList, x_loc=serIdx)

def drawSubSbplot (df, ax):
    # --- select one among the below plots
    sns.stripplot(ax=ax, data=df, jitter=True, edgecolor="gray", color=".3", alpha=min(1, 500/len(df)))
    # sns.swarmplot(ax=ax, data=df, color=".3") # --- if N is too big, use stripplot instead of swarmplot
    # --- select one among the below plots
    sns.violinplot(ax=ax, data=df)
    # sns.boxplot(ax=ax, data=df, whis=[0,100], showfliers=True, width=.25)
    # --- ex) for stripplot with hue
    # dfIdxList = [round(x/50) for x in df.index]
    # df["hl"] =  dfIdxList
    # dfIdxList = [round(x/10) for x in df.index]
    # df["de"] =  dfIdxList
    # sns.stripplot(ax=ax, data=df, y="BM_1", x="hl", hue="de")

def cm2inch(val):
    return val/2.54

def drawBoxplotPy(numChartType, dfList, nameDict, pctAddList=[], pctHideStrList=[], figsizeCm=dict(w=5, h=10)):
    assert numChartType == 1 or numChartType ==2, "1 or 2 is only supported for nuChartType ..."
    subplotRows = len(dfList[0].columns)
    (fig, axes) = plt.subplots(
        squeeze=False
        , ncols=numChartType
        , nrows=subplotRows
        , figsize=(numChartType * len(dfList) * cm2inch(figsizeCm["w"]), subplotRows * cm2inch(figsizeCm["h"])))
    plt.suptitle(nameDict["titleName"])
    for ax in axes.flat:
        ax.set(xlabel=nameDict["xAxisName"], ylabel=nameDict["yAxisName"])
    # for ax in axes.flat:
    #     ax.label_outer()
    dfM = pd.concat(dfList, axis='columns', keys=[x.name for x in dfList])
    for (colIdx, col) in enumerate(dfList[0].columns):
        # --- per a column
        df = dfM.xs(col, level=1, axis="columns")
        for chartTypeIdx in list(range(numChartType)):
            # --- N charts for same data to check other observation
            axes[colIdx, chartTypeIdx].set_title(col)
            if chartTypeIdx == 0:
                drawSubBoxplot(df, axes[colIdx, chartTypeIdx], pctAddList, pctHideStrList)
            if chartTypeIdx == 1:
                drawSubSbplot(df, axes[colIdx, chartTypeIdx])

# def initExl(xlsxFile):
#     writer = pd.ExcelWriter(xlsxFile, engine="xlsxwriter")
#     return writer
# 
# def writeExl(writer, df, sRow, sCol):
#     df.to_excel(writer, sheet_name=df.name, index=True, startrow=sRow, startcol=sCol)
# 
# def drawBoxplotExl(writer, dfList, nameDict, pctAddList=[], pctHideStrList=[]):
#     sRow = 3
#     sCol = 1
#     for df in dfList:
#         writeExl(writer, df, sRow, sCol)
#     sheetName = "chartAll"
#     worksheet = writer.book.add_worksheet(sheetName)
#     chart1 = writer.book.add_chart(dict(type='line'))
#     chart1.set_legend(dict(position='bottom'))
#     chart1.set_title(dict(name=nameDict["titleName"]))
#     chart1.set_x_axis(dict(name=nameDict["xAxisName"]))
#     chart1.set_y_axis(dict(name=nameDict["yAxisName"], min=0))
#     for df in dfList:
#         chart1.add_series(dict
#             ( values= [df.name, sRow+1, sCol+1, sRow+len(df), sCol+1]
#             )
#         )
#     sheetName = "BM_1"
#     writer.sheets[sheetName].insert_chart(sRow, sCol+5, chart1, dict(x_scale=2, yscale=1))
