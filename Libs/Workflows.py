from Libs.HEG import *
from Libs.Processes import *

class Workflows:
    
    @staticmethod
    def CMG_Workflow(hdfFile: str, removeProcessFiles: bool) -> None:
        dir_path = Util.GetDataDirectory()
        print(f"Processing: {hdfFile}")
        hdfData = hdfFile.split(".")
        DataSet = hdfData[0]
        AquisitionDate = hdfData[1]
        ProductVersion = hdfData[2]
        ProductionDate = hdfData[3]
        fileExtension = hdfData[4]
        
        print("Processing Band 1")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band1", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 1", 1, f"{DataSet}.{AquisitionDate}_Band1")
        HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band1")
        
        print("Processing Band 3")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band3", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 3", 1, f"{DataSet}.{AquisitionDate}_Band3")
        HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band3")
        
        print("Processing Band 4")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band4", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 4", 1, f"{DataSet}.{AquisitionDate}_Band4")
        HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band4")
        
        print("Processing State QA")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.StateQA", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution State QA", 1, f"{DataSet}.{AquisitionDate}_StateQA")
        HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.StateQA")
        
        print("Processing Atmosphere CM")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.CM", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Internal CM", 1, f"{DataSet}.{AquisitionDate}_CM")
        HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.CM")
        
        print("Correcting Bands")
        Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band1", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band1-Corrected")
        Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band3", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band3-Corrected")
        Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band4", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band4-Corrected")
        
        print("Composing Color")
        Processes.RGBCompose(f"{DataSet}.{AquisitionDate}_Band1-Corrected", f"{DataSet}.{AquisitionDate}_Band4-Corrected", f"{DataSet}.{AquisitionDate}_Band3-Corrected", f"{DataSet}.{AquisitionDate}_RGB")
        
        print("Generating Data Mask")
        Processes.GenerateDataMask(f"{DataSet}.{AquisitionDate}_StateQA", f"{DataSet}.{AquisitionDate}_DataMask")
        
        print("Generating No Data Mask")
        Processes.GenerateNoDataMask(f"{DataSet}.{AquisitionDate}_RGB", f"{DataSet}.{AquisitionDate}_NoData")
        
        print("Generating Sun Glint Mask")
        Processes.GenerateSunGlintMask(f"{DataSet}.{AquisitionDate}_CM", f"{DataSet}.{AquisitionDate}_GlintMask")
        
        print("Combining Masks")
        Processes.CombineMasks(f"{DataSet}.{AquisitionDate}_DataMask", f"{DataSet}.{AquisitionDate}_NoData",f"{DataSet}.{AquisitionDate}_Mask")
        Processes.CombineMasks(f"{DataSet}.{AquisitionDate}_GlintMask", f"{DataSet}.{AquisitionDate}_Mask",f"{DataSet}.{AquisitionDate}_Mask")
        
        print("Processing final image")
        Processes.ApplyMask(f"{DataSet}.{AquisitionDate}_RGB", f"{DataSet}.{AquisitionDate}_Mask", f"{DataSet}.{AquisitionDate}_Final")
        
        if removeProcessFiles == True:
            print("Removing Process Files")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}.Band1.heg")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}.Band3.heg")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}.Band4.heg")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}.StateQA.heg")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}.CM.heg")
            
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band1.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band3.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band4.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_StateQA.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_CM.tif")
            
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band1.tif.met")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band3.tif.met")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band4.tif.met")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_StateQA.tif.met")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_CM.tif.met")
            
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band1-Corrected.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band3-Corrected.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Band4-Corrected.tif")
            
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_DataMask.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_GlintMask.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_NoData.tif")
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_Mask.tif")
            
            os.remove(f"{dir_path}{DataSet}.{AquisitionDate}_RGB.tif")