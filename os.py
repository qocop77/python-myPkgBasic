import os
from datetime import datetime

def makeOutDir(prefix="Out_", outDir=None):
    dayTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not outDir:
        outDirName = prefix + dayTime
        cwdPath = os.getcwd()
        outDir = os.path.join(cwdPath, outDirName)
    os.mkdir(outDir)
    print ("Directory '{}' is created ...".format(outDir))
    return dict(dayTime=dayTime, outDir=outDir)
