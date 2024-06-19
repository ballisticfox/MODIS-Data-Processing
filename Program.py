from Libs.Workflows import *
from Libs.Processes import *
from Libs.Util import *
import wand
import wand.image
from wand.image import Image

def Main():
    files = [
        "MOD09GA.A2023245.h20v04.061.2023247025655.hdf",

    ]
    for file in files:
        Workflows.SIN_Workflow(file, False)
    
    
Main()
print("Process Complete")