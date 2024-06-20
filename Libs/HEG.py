from Libs.Util import *
import os

class HEG:

    # Generate grid data file that HEGTool can use to process HDFs into GeoTiffs
    @staticmethod
    def GenerateGrid(GRID_NAME: str, INPUT_FILENAME: str, OBJECT_NAME: str, FIELD_NAME: str, BAND_NUMBER:int, OUTPUT_PIXEL_SIZE: float, OUTPUT_FILENAME: str) -> None:
        
        # Get Data Directory
        filePath = Util.GetDataDirectory()
        fileExtension = ".hdf"
        outputFileExtension = ".tif"
        
        # Create Grid List which we will use to export to disk
        grid = []
        
        grid.append("\n")
        grid.append(f"NUM_RUNS = 1\n\n")
        grid.append(f"BEGIN\n")
        grid.append(f"INPUT_FILENAME = {filePath+INPUT_FILENAME+fileExtension}\n")
        grid.append(f"OBJECT_NAME = {OBJECT_NAME}|\n")
        grid.append(f"FIELD_NAME = {FIELD_NAME}\n")
        grid.append(f"BAND_NUMBER = {BAND_NUMBER}\n")
        grid.append(f"SPATIAL_SUBSET_UL_CORNER = ( 90.0 -180.0 )\n")
        grid.append(f"SPATIAL_SUBSET_LR_CORNER = ( -90.0 180.0 )\n")
        grid.append(f"RESAMPLING_TYPE = BI\n")
        grid.append(f"OUTPUT_PROJECTION_TYPE = GEO\n")
        grid.append(f"ELLIPSOID_CODE = WGS84\n")
        grid.append(f"OUTPUT_PROJECTION_PARAMETERS = ( 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0  )\n")
        grid.append(f"OUTPUT_PIXEL_SIZE = {OUTPUT_PIXEL_SIZE}\n")
        grid.append(f"OUTPUT_FILENAME = {filePath+OUTPUT_FILENAME+outputFileExtension}\n")
        grid.append(f"OUTPUT_TYPE = GEO\n")
        grid.append(f"END\n\n\n")
        
        # Export Grid to Disk
        with open(f".\\Data\\{GRID_NAME}.heg", "w") as file:
            for line in grid:
                file.write(line)
        
        # Correct Line Endings
        Util.correctLineEndings(f".\\Data\\{GRID_NAME}.heg")
    
    # Use a generated grid data file to convert the HDF into a GeoTiff
    @staticmethod
    def GenerateGeoTiff(GRID_FILENAME: str) -> None:
        cmd = "resample -p ./Data/" + GRID_FILENAME + ".heg -log devnull"
        os.system(cmd)