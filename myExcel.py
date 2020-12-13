from datetime import datetime
import xlsxwriter
import pandas as pd

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


def writeExcel(writer, df, sRow, sCol):
    df.to_excel(writer, sheet_name=df.name, index=True, startrow=sRow, startcol=sCol)

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
