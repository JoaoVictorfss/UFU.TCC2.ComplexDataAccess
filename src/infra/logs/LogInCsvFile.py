import csv

class LogInCsvFile:     
  @staticmethod
  def write(file, fieldnames, rows):
      with open(f"../../tests/results/{file}.csv", 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)         
        writer.writeheader()    
        for row in rows:
          writer.writerow(row)