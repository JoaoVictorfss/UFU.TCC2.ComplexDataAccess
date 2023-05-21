from datetime import datetime

BRAZIL_DATE_FORMAT = "%Y/%m/%d %H:%M"
class LogInConsole:
  @staticmethod
  def information(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"INFORMATION {datetimeStr} {message}\n")
    
  @staticmethod
  def debug(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"DEBUG {datetimeStr} {message}\n")
  
  @staticmethod
  def error(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"ERROR {datetimeStr} {message}\n")
