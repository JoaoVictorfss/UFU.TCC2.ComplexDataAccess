#File handler
class FileHandler:
    #Retrieves data from the file and returns a list containing each line of the file
    @staticmethod
    def retrieveData(path, max=None, separator=" "):    

        with open(path) as f:
          lines = []
          line_count = 0
          try:
            for line in f:
               if max is not None and line_count >= max:
                  break
               lines.append(line.rstrip().split(separator))
               line_count += 1
          finally:
            f.close()
        
        return lines