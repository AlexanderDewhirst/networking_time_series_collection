import threading
from datetime import datetime
import time
from db import helpers as db
from services.ports.scanner import Scanner

class ScannerThread(threading.Thread):
  def __init__(self, conn, current_round, round_end):
    threading.Thread.__init__(self)
    self.conn = conn
    self.current_round = current_round
    self.round_end = round_end

  def run(self):
    while datetime.now() < self.round_end:
      ports = Scanner()()

      round_port_params = []
      for i in ports:
        round_port_params.append((
          self.current_round,
          str(i),
          datetime.now(),
        ))

      # TODO: Handle struct corresponding to round data
      #   BatchService - PUT /projects/{id}/rounds/{id}
      insert_rounds_ports_query = """INSERT INTO rounds_ports(round_id, port_id, timestamp) VALUES (?, ?, ?)"""
      db.insert_many(self.conn, insert_rounds_ports_query, round_port_params)

      if datetime.now() < self.round_end:
        time.sleep(5)
