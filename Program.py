from Libs.Workflows import *
from Libs.Processes import *
from Libs.Util import *
import wand
import wand.image
from wand.image import Image

def Main():
    dir_path = Util.GetDataDirectory()
    dir_list = os.listdir(dir_path)
    
    for file in dir_list:
        print(file)
        if ".hdf" in file:
            print(file)
            Workflows.CMG_Workflow(file, True)
        
    # operator = "over"
          
    # with Image(filename=dir_path+dir_list[0]) as data:
    #     with Image(filename=dir_path+dir_list[1]) as img:
    #         data.composite(img, operator = "over")
    #     data.save(filename=dir_path+"composite.tif")
        
    # dir_list.pop(0)
    # dir_list.pop(0)
    
    # for file in dir_list:
    #     with Image(filename=dir_path+"composite.tif") as data:
    #         with Image(filename=dir_path+file) as img:
    #             data.composite(img, operator = "over")
    #         data.save(filename=dir_path+"composite.tif")
    
    
    # for file in dir_list:
    #     print(file)
    #     Workflows.CMG_Workflow(file, True)

    
        
    
    
Main()
print("Process Complete")