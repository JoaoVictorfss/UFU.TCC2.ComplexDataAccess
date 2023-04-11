import csv

class LogInCsvFile:     
  @staticmethod
  def write(file, fieldnames, rows):
      with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)         
        writer.writeheader()    
        for row in rows:
          writer.writerow(row)