from wand.image import Image
import time
from Libs.Util import *

class Processes:
    @staticmethod
    def INTtoUNIT(fileName: str, multiplier: int, gamma: float, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath = dir_path+fileName+".tif"
        with Image(filename=filePath) as img:
            img.evaluate("subtract", 32768)
            img.evaluate("multiply", 2)
            
            img.evaluate("multiply", multiplier)
            img.gamma(gamma)
            
            img.save(filename= dir_path+exportName+".tif")
    
    @staticmethod
    def RGBCompose(fileName_R: str, fileName_G: str, fileName_B: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        fileName_R = dir_path+fileName_R+".tif"
        fileName_G = dir_path+fileName_G+".tif"
        fileName_B = dir_path+fileName_B+".tif"
        
        with Image() as img:
            img.read(filename=fileName_R)
            img.read(filename=fileName_G)
            img.read(filename=fileName_B)
            img.combine(colorspace="rgb")
            img.save(filename = dir_path+exportName+".tif")
        
    @staticmethod
    def GenerateDataMask(fileName: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath = dir_path+fileName+".tif"
        
        with Image(filename=filePath) as data:
            print("Dumping to list")
            dataDump = data.export_pixels(0,0,data.width,data.height,"I","short")
            rawDataDump = []
            print("Converting to binary")
            for value in dataDump:
                rawDataDump.append(("0"*(16-len(str(bin(value))[2:]))+str(bin(value))[2:])[::-1])
            
            print("Correcting mask")
            rawCorrectedMask = []
            # index = 0
            for value in rawDataDump:
                # GoodData = True
                
                # Cloud State
                # 00 - Clear                    | 00
                # 01 - Cloudy                   | 10
                # 10 - Mixed                    | 01
                # 11 - Not Set, Assumed Clear   | 11
                # print(value)
                # print(f"{index % data.width}, {math.floor(index/data.width)}: {value}")
                # index += 1
                # print(value)
                # if value[0:] == "01" or value[-2:] == "10":
                #     GoodData = False
                #
                # 0000000000000000
                # 1111111111111111
                # 0100000000000000
                # 1100000000000000
                
                if value[6:8][::-1] == "00":
                    rawCorrectedMask.append("0000000000000000")

                if value[6:8][::-1] == "01":
                    rawCorrectedMask.append("0100000000000000")
                    
                if value[6:8][::-1] == "10":
                    rawCorrectedMask.append("1100000000000000")
                    
                if value[6:8][::-1] == "11":
                    rawCorrectedMask.append("1111111111111111")
                
                # Cloud Shadow
                # 1 - Yes
                # 0 - No
                # if value[10:11] == "0":
                #     rawCorrectedMask.append("0000000000000000")
                # else:
                #     rawCorrectedMask.append("1111111111111111")

                    
                #Land/Water Flag
                # if value[-6:-3] == 1:
                #     GoodData = False
                
                # Aersol Quantity
                # if value[-8:-6] == "00":
                #     rawCorrectedMask.append("0000000000000000")
                    
                # if value[-8:-6] == "10":
                #     rawCorrectedMask.append("1111111111111111")
                    
                # if value[-8:-6] == "01":
                #     rawCorrectedMask.append("0100000000000000")
                    
                # if value[-8:-6] == "11":
                #     rawCorrectedMask.append("1100000000000000")
                    
                
                
                # #Cirrus Detected
                # if value[-8:-6] == "11":
                #     GoodData = False
                
                
                # print(value)

                # if value[0:2] == "10":
                #     GoodData = True
                
                # if value[2:3] == "1":
                #     GoodData = False
                # if value[10:11] == '1':
                #     GoodData = False
                    
                # if GoodData == True:
                    # rawCorrectedMask.append("0000000000000000")
                # else:
                #     rawCorrectedMask.append("1111111111111111")
                
            
            print("Converting mask to integer")
            CorrectedMask = []
            for value in rawCorrectedMask:
                CorrectedMask.append(int(value, 2))
            
            print("Dumping mask")
            data.import_pixels(0,0,data.width,data.height,"I","short",CorrectedMask)
            
            print("Exporting Image")
            # data.negate()
            data.save(filename=dir_path+exportName+".tif")
    
    
    @staticmethod
    def GenerateSunGlintMask(fileName: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath = dir_path+fileName+".tif"

        with Image(filename=filePath) as data:
            print("Dumping to list")
            dataDump = data.export_pixels(0,0,data.width,data.height,"I","short")
            rawDataDump = []
            print("Converting to binary")
            for value in dataDump:
                rawDataDump.append("0"*(16-len(str(bin(value))[2:]))+str(bin(value))[2:])
            
            print("Correcting mask")
            rawCorrectedMask = []
            # index = 0
            for value in rawDataDump:
                GoodData = True
                
                # print(value[-8:-7])
                if value[-7:-6] == "1":
                    GoodData = False
                    
                    
                if GoodData == True:
                    rawCorrectedMask.append("0000000000000000")
                else:
                    rawCorrectedMask.append("1111111111111111")
                
            print("Converting mask to integer")
            CorrectedMask = []
            for value in rawCorrectedMask:
                CorrectedMask.append(int(value, 2))
            
            print("Dumping mask")
            data.import_pixels(0,0,data.width,data.height,"I","short",CorrectedMask)
            
            print("Exporting Image")
            # data.negate()
            data.negate()
            data.save(filename=dir_path+exportName+".tif")
            
    
    @staticmethod
    def GenerateNoDataMask(fileName: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath = dir_path+fileName+".tif"

        with Image(filename=filePath) as data:
            dataDump = data.export_pixels(0,0,data.width,data.height,"I","short")
            
            Mask = []
            for value in dataDump:
                if value > 0:
                    Mask.append(int(65535))
                else:
                    Mask.append(int(0))
            
            data.import_pixels(0,0,data.width,data.height,"I","short",Mask)
            data.save(filename=dir_path+exportName+".tif")
            
    @staticmethod
    def CombineMasks(fileName1: str, fileName2: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath1 = dir_path+fileName1+".tif"
        filePath2 = dir_path+fileName2+".tif"
        
        with Image(filename=filePath1) as data1:
            with Image(filename=filePath2) as data2:
                data2.negate()
                data1.composite(data2, operator='minus_src')
                
            data1.save(filename=dir_path+exportName+".tif")
    
    
    
    
    @staticmethod
    def ApplyMask(fileName: str, maskName: str, exportName: str) -> None:
        dir_path = Util.GetDataDirectory()
        filePath = dir_path+fileName+".tif"
        maskPath = dir_path+maskName+".tif"
        
        with Image(filename = filePath) as img:
            img.alpha_channel = True
            with Image(filename = maskPath) as mask:
                img.composite(mask, operator="copy_alpha")
            
            img.save(filename=dir_path+exportName+".tif")
            