import socket

class Scanner:
  def __init__(self):
    self.ports = []
    self.ip = socket.gethostbyname('')

  def __call__(self):
    for port in range(1,65535):
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, port))
      except:
        self.ports.append(port)
      s.close()
    return self.ports
