from datetime import datetime

class LogInConsole:
  @staticmethod
  def information(message):
    print(f"INFORMATION {datetime.utcnow()} {message}")
    
  @staticmethod
  def debug(message):
    print(f"DEBUG {datetime.utcnow()} {message}")
  
  @staticmethod
  def error(message):
    print(f"ERROR {datetime.utcnow()} {message}")
