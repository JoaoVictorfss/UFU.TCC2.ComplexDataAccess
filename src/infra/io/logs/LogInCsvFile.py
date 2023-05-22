import csv
import os

#Log class for csv file
class LogInCsvFile:     
  @staticmethod
  def write(file, fieldnames, rows):
      directory = os.path.dirname(file)
      if directory:
        os.makedirs(directory, exist_ok=True)
                    
      with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)         
        writer.writeheader()    
        for row in rows:
          writer.writerow(row)