class Tile:
    # Stores data read from CSVs downloaded off of https://ladsweb.modaps.eosdis.nasa.gov/search/
    
    fileName: str
    url: str
    size: int
    dataSet: str
    productName: str
    aquisitionDate: str
    gridCoord: str
    productVersion: str
    productionDate: str
    fileExtension: str
    
    def __init__(self, line: str) -> None:
        ###
        #
        #   Data from urls are recieved in this format:
        #      0      1     2
        #   fileID | URL | Size
        #
        #   Data in URL is formatted in this format:
        #      0         1         2         3        4        5      6       7
        #     Null | archive | allData | Unknown | Dataset | Year | Date | FileName
        #
        #   Data product names are formatted as:
        #      0           1                2           3               4           5
        #   DataSet | AquisitionData | GridCoord | ProductVersion |UploadDate | FileType
        #
        ###
        
        data: list[str]
        linkData: list[str]
        
        data = line.split(",")
        linkData = data[1].split("/")
        nameData = linkData[7].split(".")
        
        self.fileName = linkData[7]
        
        self.dataSet = nameData[0]
        self.productName = nameData[0][0:-2]
        self.aquisitionDate = nameData[1]
        self.gridCoord = nameData[2]
        self.productVersion = nameData[3]
        self.productionDate = nameData[4]
        self.fileExtension = nameData[5]
        
        self.url = data[1]
        self.size = int(data[2])
        