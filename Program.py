from Libs.Workflows import *
from Libs.Processes import *
from Libs.Util import *
from Libs.Networking import *
from Libs.Tile import *

def Main():
    tileList = Networking.ProcessCSV("LAADS_query.2024-06-20T05_11.csv")
    for tile in tileList:
        print(tile.productName)
    
Main()
print("Process Complete")