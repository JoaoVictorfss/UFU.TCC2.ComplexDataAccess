import csv
import os

#Log class for csv file
class LogInCsvFile:     
  @staticmethod
  def write(file, fieldnames, rows):   
      mode = 'a' if os.path.exists(file) else 'w'

      directory = os.path.dirname(file)
      if directory:
        os.makedirs(directory, exist_ok=True)
                    
      with open(file, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
        
        if(mode == 'w'): writer.writeheader()    
        
        for row in rows:
          writer.writerow(row)