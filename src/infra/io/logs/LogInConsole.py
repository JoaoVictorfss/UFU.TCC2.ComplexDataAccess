from datetime import datetime

BRAZIL_DATE_FORMAT = "%Y/%m/%d %H:%M"

#Log class for console
class LogInConsole:
  @staticmethod
  def information(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"\033[93m{datetimeStr} {message}\033[0m\n")
    
  @staticmethod
  def debug(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"\033[37m{datetimeStr} {message}\033[0m\n")
  
  @staticmethod
  def error(message):
    datetimeStr = datetime.now().strftime(BRAZIL_DATE_FORMAT)
    print(f"\033[91m{datetimeStr} {message}\033[0m\n")
