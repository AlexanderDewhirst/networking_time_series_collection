from datetime import datetime

class Log():
  def __init__(self, message):
    self.message = message
    self()

  def __call__(self):
    now = datetime.now()
    print(now, self.message)
