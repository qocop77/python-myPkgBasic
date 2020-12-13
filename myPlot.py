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

def drawLineplotSb(ax, df, labelDict={}):
    sns.lineplot(ax=ax, data=df)
    _setLabel(ax, labelDict)

def drawBoxplotSb(ax, df, labelDict={}):
    sns.stripplot(ax=ax, data=df, jitter=True, edgecolor="gray", color=".3", alpha=min(1, 500 / len(df)))
    # sns.swarmplot(ax=ax, data=df, color=".3") # --- if N is too big, use stripplot instead of swarmplot
    # sns.violinplot(ax=ax, data=df)
    sns.boxplot(ax=ax, data=df, whis=1.5, showmeans=True, showfliers=True, width=0.25)
    _setLabel(ax, labelDict)

# --- if userPctList, max
def drawBoxplotDf(ax, df, annoPctList=["max", "75%", "50%", "mean"], userPctList=[], labelDict={}):
    if not userPctList:
        bpdict = df.boxplot(
            ax=ax
            , return_type="dict"
            , column=df.columns.to_list()
            , flierprops=dict(markerfacecolor="r", marker="s")
            , fontsize=5
            , showmeans=True
            , showfliers=True
        )
    else:
        dfStats = df.describe(percentiles=[float(x) / 100 for x in ([0,25,50,75,100] + userPctList)])
        userPctStrList = ["{}%".format(userPct) for userPct in userPctList]
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
                , fontsize=5
            )]
        bpdict = ax.bxp(boxes, showmeans=True, showfliers=True)
    ymaxLim = -sys.maxsize - 1
    for (serIdx, _) in enumerate(df):
        ymax = _annBoxplot(bpdict, ax, serIdx, userPctList, annoPctList)["max"]
        ymaxLim = ymax if ymaxLim < ymax else ymaxLim
    ax.set_ylim(ymax=ymaxLim * 1.2)
    _setLabel(ax, labelDict)

def makeSubplots (nRows, nCols, nSers, labelDict={}):
    figSize = (nSers * _cm2inch(5), _cm2inch(15))
    if nRows == nCols == 1:
        axes = np.ndarray(shape=(1,1), dtype=object)
        fig = plt.figure(figsize=figSize)
        axes[0][0] = fig.add_axes([0.10, 0.10, 0.80, 0.80]) 
    else:
        (fig, axes) = plt.subplots(squeeze=False, nrows=nRows, ncols=nCols, figsize=figSize)
    for ax in axes.flat:
        _setLabel(ax, labelDict)
        ax.grid(axis="y")
    return (fig, axes)

# ====================================================================================================
# Private
# ====================================================================================================

def _setLabel (ax, labelDict):
    if labelDict.get("title"):
        ax.set_title(labelDict.get("title"), fontsize=10)
    if labelDict.get("xlabel"):
        ax.set_title(labelDict.get("xlabel"), fontsize=7)
    if labelDict.get("ylabel"):
        ax.set_title(labelDict.get("ylabel"), fontsize=7)

def _cm2inch(val):
    return val / 2.54

def _annBoxplot(
    bpdict, ax, x_loc
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
        yDict["{}%".format(userPct)] = bpdict["fliers"][x_loc].get_ydata()[idx]
    for annoPct in annoPctList:
        annoStr = annoPct
        annoStr = "max@1.5IQR" if not userPctList and annoStr == "max" else annoStr
        annoStr = "min@1.5IQR" if not userPctList and annoStr == "min" else annoStr
        ax.annotate(
            "{} : {}".format(annoStr, np.round(yDict[annoPct], 2))
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
