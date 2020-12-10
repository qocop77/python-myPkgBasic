import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
import myPkgBasic.myOs as myBasicOs


def annotateBoxplot(bpdict, ax, pctStrList, pctHideStrList, x_loc=0):
    valList = []
    valList += [bpdict["means"][x_loc].get_ydata()[0]]  # means
    valList += [bpdict["caps"][x_loc * 2].get_ydata()[0]]  # min
    valList += [bpdict["boxes"][x_loc].get_ydata()[0]]  # 25%
    valList += [bpdict["medians"][x_loc].get_ydata()[0]]  # 50%
    valList += [bpdict["boxes"][x_loc].get_ydata()[2]]  # 75%
    valList += [bpdict["caps"][(x_loc * 2) + 1].get_ydata()[0]]  # max
    for (idx, _) in enumerate(pctStrList[6:]):
        valList += [bpdict["fliers"][x_loc].get_ydata()[idx]]
    x_offset=0.05
    x_text = 15
    ha = "left"
    for (idx, pctStr) in reversed(list(enumerate(pctStrList))):
        isAnno = True
        isAnno &= (pctStr not in pctHideStrList)
        if idx < len(pctStrList)-1:
            isAnno &= (abs(valList[idx]-valList[idx+1]) > 100)
        if not pctStr in pctHideStrList:
            ax.annotate(
                "{} : {}".format(pctStr, np.round(valList[idx], 2)),
                (x_loc + 1 + x_offset, valList[idx]),
                **{"xytext": (x_text, 100), "textcoords": "offset pixels", "ha": ha, "arrowprops": {"arrowstyle": "->"}}
            )
            x_offset = -x_offset
            x_text = -x_text 
            ha = "right" if ha == "left" else "left"
    return {"75%": valList[4], "max": valList[5]}


def drawSubSbplot(df, ax):
    sns.stripplot(
        ax=ax,
        data=df,
        jitter=True,
        edgecolor="gray",
        color=".3",
        alpha=min(1, 500 / len(df)),
    )
    # sns.swarmplot(ax=ax, data=df, color=".3") # --- if N is too big, use stripplot instead of swarmplot
    # sns.violinplot(ax=ax, data=df)
    sns.boxplot(ax=ax, data=df, whis=1.5, showmeans=True, showfliers=True, width=0.25)


def drawSubBoxplot(df, ax, pctHideStrList=[]):
    pctDefStrList = ["mean", "min_1.5IQR", "25%", "50%", "75%", "max_1.5IQR"]
    bpdict = df.boxplot(
        ax=ax,
        return_type="dict",
        column=df.columns.to_list(),
        showmeans=True,
        showfliers=True,
        notch=False,
        fontsize=7,
        flierprops=dict(markerfacecolor="r", marker="s"),
    )
    ylimMax = -sys.maxsize - 1
    for (serIdx, _) in enumerate(df):
        pctStrList = pctDefStrList
        ylim = annotateBoxplot(bpdict, ax, pctDefStrList, pctHideStrList, serIdx)["max"]
        ylimMax = ylim if ylimMax < ylim else ylimMax
    ax.set_ylim(ymax=ylimMax * 1.2)


def drawSubBoxplotCustom(df, ax, pctAddList=[], pctHideStrList=[]):
    pctDefList = [0, 25, 50, 75, 100]
    pctDefStrList = ["mean", "min", "25%", "50%", "75%", "max"]
    pctAddStrList = [str(pctAdd) + "%" for pctAdd in pctAddList]
    dfStats = df.describe(
        percentiles=[float(x) / 100 for x in (pctDefList + pctAddList)]
    )
    boxes = []
    for dfName in dfStats:
        boxes += [
            dict(
                label="{} (N={})".format(dfName, int(dfStats[dfName].loc["count"])),
                whis="range",
                mean=dfStats[dfName].loc[pctDefStrList[0]],
                whislo=dfStats[dfName].loc[pctDefStrList[1]],
                q1=dfStats[dfName].loc[pctDefStrList[2]],
                med=dfStats[dfName].loc[pctDefStrList[3]],
                q3=dfStats[dfName].loc[pctDefStrList[4]],
                whishi=dfStats[dfName].loc[pctDefStrList[5]],
                fliers=dfStats[dfName].loc[pctAddStrList],
                flierprops=dict(markerfacecolor="r", marker="s"),
                fontsize=7,
            )
        ]
    bpdict = ax.bxp(boxes, showmeans=True, showfliers=True)
    ylimMax = -sys.maxsize - 1
    for (serIdx, _) in enumerate(df):
        pctStrList = pctDefStrList + pctAddStrList
        ylim = annotateBoxplot(bpdict, ax, pctStrList, pctHideStrList, serIdx)["max"]
        ylimMax = ylim if ylimMax < ylim else ylimMax
    ax.set_ylim(ymax=ylimMax * 1.2)


def cm2inch(val):
    return val / 2.54


def drawBoxplotPy(
    ctypeList,
    dfList,
    nameDict,
    pctAddList=[],
    pctHideStrList=[],
    figsizeCm=dict(w=5, h=10),
):
    subplotRows = len(dfList[0].columns)
    (fig, axes) = plt.subplots(
        squeeze=False,
        ncols=len(ctypeList),
        nrows=subplotRows,
        figsize=(
            len(ctypeList) * len(dfList) * cm2inch(figsizeCm["w"]),
            subplotRows * cm2inch(figsizeCm["h"]),
        ),
    )
    plt.suptitle(nameDict["titleName"])
    for ax in axes.flat:
        ax.set(xlabel=nameDict["xAxisName"], ylabel=nameDict["yAxisName"])
    # for ax in axes.flat:
    #     ax.label_outer()
    dfM = pd.concat(dfList, axis="columns", keys=[x.name for x in dfList])
    for (colIdx, col) in enumerate(dfList[0].columns):
        # --- per a column
        df = dfM.xs(col, level=1, axis="columns")
        for (ctypeIdx, cType) in enumerate(ctypeList):
            ax = axes[colIdx, ctypeIdx]
            ax.set_title(col)
            if cType == 0:
                drawSubSbplot(df, ax)
            elif cType == 1:
                drawSubBoxplot(df, ax, pctHideStrList)
            elif cType == 2:
                drawSubBoxplotCustom(df, ax, pctAddList, pctHideStrList)


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
