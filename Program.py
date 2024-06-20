from Libs.Workflows import *
from Libs.Processes import *
from Libs.Util import *
from Libs.Networking import *
from Libs.Tile import *
from Libs.Token import *

def Main():
    tileList = Networking.ProcessCSV("LAADS_query.2024-06-20T05_40.csv")
    for tile in tileList:
        print(tile.productName)
        Networking.downloadURL(tile, Token.GetToken())
    
    for index in range(0,int(len(tileList)/2)):
        print(tileList[index].fileName)
        Workflows.MOD09("MYD09", tileList[index].fileName, True)
    
Main()
print("Process Complete")