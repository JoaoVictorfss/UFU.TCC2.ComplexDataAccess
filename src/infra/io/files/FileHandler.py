#File handler
class FileHandler:
    #Retrieves data from the file and returns a list containing each line of the file
    @staticmethod
    def retrieveData(path, separator=" "):        
        with open(path) as f:
          lines = [line.rstrip().split(separator) for line in f]
        
        return lines