from datetime import datetime
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
import myPkgBasic.myPlot as myBasicPlot

# ====================================================================================================
# Public
# ====================================================================================================

def initExcel(outFile):
    writer = pd.ExcelWriter(outFile, engine="xlsxwriter")
    dayTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame([{"Created : ": dayTime}])
    df.name = "Output"
    df.T.to_excel(writer, sheet_name=df.name, header=False, index=True, startrow=0, startcol=0)
    return writer

def closeExcel(writer):
    outFile = writer.book.filename
    print ("Create output file of {}".format(outFile))
    writer.close()

def writeDfMyplot (figFile, scaleDict, locDict, outSName, writer):
    writer.sheets[outSName].insert_image(locDict["row"], locDict["col"], figFile, scaleDict)

def writeDfChart (df, cType, labelDict, scaleDict, locDict, outSName, writer):
    dataRow = 3
    dataCol = 1
    dataSName = df.name
    worksheet = writer.book.get_worksheet_by_name(dataSName)
    if worksheet is None:
        df.to_excel(writer, sheet_name=dataSName, index=True, startrow=dataRow, startcol=dataCol)
    if cType == 1:
        chart = writer.book.add_chart(dict(type='line'))
    else:
        chart = writer.book.add_chart(dict(type='line'))
    _setLabel(chart, labelDict)
    chart.set_legend({"position": 'bottom'})
    for colIdx in range(len(df.columns)):
        chart.add_series(dict(
            name=[dataSName, dataRow, dataCol+colIdx+1]
            , values=[dataSName, dataRow+1, dataCol+colIdx+1, dataRow+len(df), dataCol+colIdx+1]
            , marker={'type': 'automatic'}
        ))
    writer.sheets[outSName].insert_chart(locDict["row"], locDict["col"], chart, scaleDict)

# ====================================================================================================
# Private
# ====================================================================================================

def _setLabel (chart, labelDict):
    if labelDict.get("title"):
        chart.set_title({"name": labelDict.get("title")})
    if labelDict.get("xlabel"):
        chart.set_x_axis({"name": labelDict.get("xlabel")})
    if labelDict.get("ylabel"):
        chart.set_y_axis({"name": labelDict.get("ylabel")})
