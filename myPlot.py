import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
import myPkgBasic.myOs as myBasicOs

# ====================================================================================================
# Public
# ====================================================================================================

def drawLineplotSb(ax, df):
    sns.lineplot(ax=ax, data=df)

def drawBoxplotSb(ax, df):
    sns.stripplot(ax=ax, data=df, jitter=True, edgecolor="gray", color=".3", alpha=min(1, 500 / len(df)))
    # sns.swarmplot(ax=ax, data=df, color=".3") # --- if N is too big, use stripplot instead of swarmplot
    # sns.violinplot(ax=ax, data=df)
    sns.boxplot(ax=ax, data=df, whis=1.5, showmeans=True, showfliers=True, width=0.25)

def drawBoxplotDf(ax, df, annoPctList=["max", "75%", "50%", "mean"], userPctList=[]):
    if not userPctList:
        bpdict = df.boxplot(
            ax=ax
            , return_type="dict"
            , column=df.columns.to_list()
            , flierprops=dict(markerfacecolor="r", marker="s")
            , fontsize=7
            , showmeans=True
            , showfliers=True
        )
    else:
        print (df)
        dfStats = df.describe(percentiles=[float(x) / 100 for x in ([0,25,50,75,100] + userPctList)])
        userPctStrList = ["{}%".format(userPct) for userPct in userPctList]
        print (userPctStrList)
        boxes = []
        for col in dfStats:
            boxes += [dict(
                label="{} (N={})".format(col, int(dfStats[col].loc["count"]))
                , whis="range"
                , mean=dfStats[col].loc["mean"]
                , whislo=dfStats[col].loc["min"]
                , q1=dfStats[col].loc["25%"]
                , med=dfStats[col].loc["50%"]
                , q3=dfStats[col].loc["75%"]
                , whishi=dfStats[col].loc["max"]
                , fliers=dfStats[col].loc[userPctStrList]
                , flierprops=dict(markerfacecolor="r", marker="s")
                , fontsize=7
            )]
        bpdict = ax.bxp(boxes, showmeans=True, showfliers=True)
        print (col)
        print (dfStats)
        print (dfStats[col])
        print (dfStats[col].loc["90%"])
        print (str(dfStats[col].loc[userPctStrList]))
    ymaxLim = -sys.maxsize - 1
    for (serIdx, _) in enumerate(df):
        ymax = _annBoxplot(bpdict, ax, serIdx, userPctList, annoPctList)["max"]
        ymaxLim = ymax if ymaxLim < ymax else ymaxLim
    ax.set_ylim(ymax=ymaxLim * 1.2)

def makeSubplots (nRows, nCols, nSers):
    figSize = (nSers * _cm2inch(15), nRows * _cm2inch(15))
    (fig, axes) = plt.subplots(squeeze=False, nrows=nRows, ncols=nCols, figsize=figSize)
    return (fig, axes)

# def initExl(xlsxFile):
#     writer = pd.ExcelWriter(xlsxFile, engine="xlsxwriter")
#     return writer
#
# def writeExl(writer, df, sRow, sCol):
#     df.to_excel(writer, sheet_name=df.name, index=True, startrow=sRow, startcol=sCol)
#
# def drawBoxplotExl(writer, dfList, nameDict, pctAddList=[], annoPctList=[]):
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

# ====================================================================================================
# Private
# ====================================================================================================

def _cm2inch(val):
    return val / 2.54

def _annBoxplot(
    bpdict, ax, x_loc=0
    , userPctList=[]
    , annoPctList=["max", "75%", "50%", "25%", "min", "mean"]
    , x_offset=0.05, x_text=20, y_text=30, ha="left"
):
    yDict = {}
    yDict["max"] = bpdict["caps"][(x_loc * 2) + 1].get_ydata()[0]
    yDict["75%"] = bpdict["boxes"][x_loc].get_ydata()[2]
    yDict["50%"] = bpdict["medians"][x_loc].get_ydata()[0]
    yDict["25%"] = bpdict["boxes"][x_loc].get_ydata()[0]
    yDict["min"] = bpdict["caps"][x_loc * 2].get_ydata()[0]
    yDict["mean"] = bpdict["means"][x_loc].get_ydata()[0]
    for (idx, userPct) in enumerate(userPctList):
        yDict["{}%".format(userPct)] += [bpdict["fliers"][x_loc].get_ydata()[idx]]
    for annoPct in annoPctList:
        ax.annotate(
            "{} : {}".format(annoPct, np.round(yDict[annoPct], 2))
            , (x_loc + 1 + x_offset, yDict[annoPct])
            , **{
                "xytext": (x_text, y_text)
                , "textcoords": "offset pixels"
                , "ha": ha
                , "arrowprops": {"arrowstyle": "->"}
            }
        )
        x_offset = -x_offset
        x_text = -x_text 
        y_text = -y_text if x_text > 0 else y_text
        ha = "right" if ha == "left" else "left"
    return {"75%": yDict["75%"], "max": yDict["max"]}
