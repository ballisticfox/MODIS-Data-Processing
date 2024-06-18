import os

class Util:
    @staticmethod
    def clearConsole() -> None:
        os.system('cls')

    @staticmethod
    def GetDataDirectory() -> str:
        # Find where we are
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.split("\\")
        dir_path.pop(len(dir_path)-1)
        
        data_path = ""
        for folder in dir_path:
            data_path += folder+"\\"
        data_path += "Data\\"
        
        return data_path
    
    # Convert to unix line endings
    @staticmethod
    def correctLineEndings(fileName: str) -> None:
        WINDOWS_LINE_ENDING = b'\r\n'
        UNIX_LINE_ENDING = b'\n'
        
        with open(fileName, 'rb') as open_file:
            content = open_file.read()
        
        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        
        with open(fileName, 'wb') as open_file:
            open_file.write(content)