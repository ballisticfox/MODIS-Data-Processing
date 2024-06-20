class Tile:
    name: str
    url: str
    size: int
    
    def __init__(self, line: str) -> None:
        ###
        #   Data from urls are recieved in this format:
        #      0      1     2
        #   fileID | URL | Size
        #
        #   Data in URL is formatted in this format:
        #      0         1         2         3        4        5      6       7
        #     Null | archive | allData | Unknown | Dataset | Year | Date | FileName
        #
        #
        ###
        data: list[str]
        linkData: list[str]
        
        data = line.split(",")
        linkData = data[1].split("/")
        nameData = linkData[7].split(".")
        
        self.filename = linkData[7]
        self.name = nameData[2]
        self.url = data[1]
        self.size = int(data[2])
        