import os
from datetime import datetime

def makeOutDir(outDir=None):
    if not outDir:
        dayTime = datetime.now().strftime("%Y%m%d_%H%M%S")
        outDirName = "Out_" + dayTime
        cwdPath = os.getcwd()
        outDir = os.path.join(cwdPath, outDirName)
    os.mkdir(outDir)
    print ("Directory '{}' is created ...".format(outDir))
    return dict(dayTime=dayTime, outDir=outDir)