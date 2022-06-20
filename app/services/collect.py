from datetime import datetime, timedelta
from db import helpers as db
from services.log import Log
from threads.scanner_thread import ScannerThread
from threads.sniffer_thread import SnifferThread

class Collect():
  def __init__(self, conn):
    self.conn = conn
    self.round_start = datetime.now()

  def __call__(self):
    round_end = self.round_start + timedelta(0, 60)
    current_round = self.__create_round()
    Log("Round starting " + str(current_round))

    # Collect network traffic
    thread1 = ScannerThread(self.conn, current_round, round_end)
    thread2 = SnifferThread(self.conn, current_round, round_end)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    Log("Round completed successfully")

  def __create_round(self):
    insert_round_query = """INSERT INTO rounds(start_time) values (?)"""
    db.insert(self.conn, insert_round_query, (str(self.round_start.isoformat()),))

    # Get round
    select_round_query = """SELECT id FROM rounds WHERE start_time = ?"""
    current_round = db.select(self.conn, select_round_query, (str(self.round_start.isoformat()),))[0][0]
    return current_round
