import requests
import sys
from Tile import *
from Util import *

class Networking:
    
    # Parses CSVs downloaded from: https://ladsweb.modaps.eosdis.nasa.gov/search/
    @staticmethod
    def ProcessCSV(fileName: str):
        dir_path = Util.GetDataDirectory()
        
        rawData = []
        tileList = []
        
        
        with open(dir_path+fileName, 'r') as csv:
            for line in csv:
                rawData.append(line)
        
        rawData.pop(0)
        
        for tile in rawData:
            tileData = Tile(tile)
            tileList.append(tileData)
        
        return tileList


    # Takes in a tile and downloads it from the URL, you must generate a token using your EarthData Login
    @staticmethod
    def downloadURL(tile: Tile, token: str) -> None:
        dir_path = Util.GetDataDirectory()
        
        prefix: str = "https://ladsweb.modaps.eosdis.nasa.gov"
        fullURL: str = prefix + tile.url
        packageSize: int = 0
        
        print("Downloading: " + tile.name)
        
        with requests.get(fullURL, stream=True, headers={'Authorization': 'Bearer ' + token}) as r:
            r.raise_for_status()
            print(r.url)
            print(r.status_code)

            with open(dir_path+tile.filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        packageSize += 8192
                        print(f"Downloaded {packageSize/1024**2:.2f} mb / {tile.size/1024**2:.2f}mb / {packageSize/tile.size*100:.1f}%")
                        sys.stdout.write("\033[F")
