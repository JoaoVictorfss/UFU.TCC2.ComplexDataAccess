class FileHandler:
    @staticmethod
    def retrieveData(path, separator=" "):        
        with open(path) as f:
          lines = [line.rstrip().split(separator) for line in f]
        
        return lines