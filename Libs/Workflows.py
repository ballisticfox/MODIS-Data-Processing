from Libs.HEG import *
from Libs.Processes import *
import threading

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
        
        # Level 0
        print("Processing Grids")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band1", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 1", 1, f"{DataSet}.{AquisitionDate}_Band1")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band3", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 3", 1, f"{DataSet}.{AquisitionDate}_Band3")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.Band4", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Surface Reflectance Band 4", 1, f"{DataSet}.{AquisitionDate}_Band4")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.StateQA", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution State QA", 1, f"{DataSet}.{AquisitionDate}_StateQA")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.CM", f"{DataSet}.{AquisitionDate}.{ProductVersion}.{ProductionDate}", f"{DataSet}", "Coarse Resolution Internal CM", 1, f"{DataSet}.{AquisitionDate}_CM")
        
        
        
        # Level 1
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band1")
        t1 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.Band1",))
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band3")
        t2 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.Band3",))
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band4")
        t3 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.Band4",))
        
        #HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.StateQA")
        t4 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.StateQA",))
        #HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.CM")
        t5 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.CM",))
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
        # Level 2
        # print("Correcting Bands")
        # Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band1", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band1-Corrected")
        # Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band3", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band3-Corrected")
        # Processes.INTtoUNIT(f"{DataSet}.{AquisitionDate}_Band4", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band4-Corrected")
        t6 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{AquisitionDate}_Band1", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band1-Corrected",))
        t7 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{AquisitionDate}_Band3", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band3-Corrected",))
        t8 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{AquisitionDate}_Band4", 2, 2.2, f"{DataSet}.{AquisitionDate}_Band4-Corrected",))
        
        t6.start()
        t7.start()
        t8.start()
        
        t6.join()
        t7.join()
        t8.join()
        
        print("Composing Color")
        Processes.RGBCompose(f"{DataSet}.{AquisitionDate}_Band1-Corrected", f"{DataSet}.{AquisitionDate}_Band4-Corrected", f"{DataSet}.{AquisitionDate}_Band3-Corrected", f"{DataSet}.{AquisitionDate}_RGB")
        
        
        # Level 3
        
        # print("Generating Data Mask")
        # Processes.GenerateDataMask(f"{DataSet}.{AquisitionDate}_StateQA", f"{DataSet}.{AquisitionDate}_DataMask")
        t9 = threading.Thread(target=Processes.GenerateDataMask, args=(f"{DataSet}.{AquisitionDate}_StateQA", f"{DataSet}.{AquisitionDate}_DataMask",))
        
        # print("Generating No Data Mask")
        # Processes.GenerateNoDataMask(f"{DataSet}.{AquisitionDate}_RGB", f"{DataSet}.{AquisitionDate}_NoData")
        t10 = threading.Thread(target=Processes.GenerateNoDataMask, args=(f"{DataSet}.{AquisitionDate}_RGB", f"{DataSet}.{AquisitionDate}_NoData",))
        
        # print("Generating Sun Glint Mask")
        # Processes.GenerateSunGlintMask(f"{DataSet}.{AquisitionDate}_CM", f"{DataSet}.{AquisitionDate}_GlintMask")
        t11 = threading.Thread(target=Processes.GenerateSunGlintMask, args=(f"{DataSet}.{AquisitionDate}_CM", f"{DataSet}.{AquisitionDate}_GlintMask",))
        
        t9.start()
        t10.start()
        t11.start()
        
        t9.join()
        t10.join()
        t11.join()
        
        
        # Level 4
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
        
    @staticmethod    
    def SIN_Workflow(hdfFile: str, removeProcessFiles: bool) -> None:
        dir_path = Util.GetDataDirectory()
        print(f"Processing: {hdfFile}")
        hdfData = hdfFile.split(".")
        print(hdfData)
        DataSet = hdfData[0]
        AquisitionDate = hdfData[1]
        GridCoord = hdfData[2]
        ProductVersion = hdfData[3]
        ProductionDate = hdfData[4]
        fileExtension = hdfData[5]
        
        
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band1", f"{DataSet}.{AquisitionDate}.{GridCoord}.{ProductVersion}.{ProductionDate}", "MODIS_Grid_500m_2D", "sur_refl_b01_1", 1, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band1")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band3", f"{DataSet}.{AquisitionDate}.{GridCoord}.{ProductVersion}.{ProductionDate}", "MODIS_Grid_500m_2D", "sur_refl_b03_1", 1, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band3")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band4", f"{DataSet}.{AquisitionDate}.{GridCoord}.{ProductVersion}.{ProductionDate}", "MODIS_Grid_500m_2D", "sur_refl_b04_1", 1, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band4")
        HEG.GenerateGrid(f"{DataSet}.{AquisitionDate}.{GridCoord}.StateQA", f"{DataSet}.{AquisitionDate}.{GridCoord}.{ProductVersion}.{ProductionDate}", "MODIS_Grid_1km_2D", "state_1km_1", 1, f"{DataSet}.{GridCoord}.{AquisitionDate}_StateQA")

        # Level 1
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band1")
        t1 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band1",))
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band3")
        t2 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band3",))
        # HEG.GenerateGeoTiff(f"{DataSet}.{AquisitionDate}.Band4")
        t3 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.{GridCoord}.Band4",))
        
        t4 = threading.Thread(target=HEG.GenerateGeoTiff, args=(f"{DataSet}.{AquisitionDate}.{GridCoord}.StateQA",))

        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        
        t6 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{GridCoord}.{AquisitionDate}_Band1", 2, 2.2, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band1-Corrected",))
        t7 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{GridCoord}.{AquisitionDate}_Band3", 2, 2.2, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band3-Corrected",))
        t8 = threading.Thread(target=Processes.INTtoUNIT, args=(f"{DataSet}.{GridCoord}.{AquisitionDate}_Band4", 2, 2.2, f"{DataSet}.{GridCoord}.{AquisitionDate}_Band4-Corrected",))
        
        t6.start()
        t7.start()
        t8.start()
        
        t6.join()
        t7.join()
        t8.join()
        
        print("Composing Color")
        Processes.RGBCompose(f"{DataSet}.{GridCoord}.{AquisitionDate}_Band1-Corrected", f"{DataSet}.{GridCoord}.{AquisitionDate}_Band4-Corrected", f"{DataSet}.{GridCoord}.{AquisitionDate}_Band3-Corrected", f"{DataSet}.{GridCoord}.{AquisitionDate}_RGB")
        
        # Level 3
        
        # print("Generating Data Mask")
        # Processes.GenerateDataMask(f"{DataSet}.{AquisitionDate}_StateQA", f"{DataSet}.{AquisitionDate}_DataMask")
        t9 = threading.Thread(target=Processes.GenerateDataMask, args=(f"{DataSet}.{GridCoord}.{AquisitionDate}_StateQA", f"{DataSet}.{GridCoord}.{AquisitionDate}_DataMask",))
        
        # print("Generating No Data Mask")
        # Processes.GenerateNoDataMask(f"{DataSet}.{AquisitionDate}_RGB", f"{DataSet}.{AquisitionDate}_NoData")
        t10 = threading.Thread(target=Processes.GenerateNoDataMask, args=(f"{DataSet}.{GridCoord}.{AquisitionDate}_RGB", f"{DataSet}.{GridCoord}.{AquisitionDate}_NoData",))
        
        t9.start()
        t10.start()
        
        t9.join()
        t10.join()