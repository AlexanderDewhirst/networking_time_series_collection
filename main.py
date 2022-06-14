from datetime import datetime, timedelta
from db import helpers as db
from threads.scanner_thread import ScannerThread
from threads.sniffer_thread import SnifferThread

if __name__ == "__main__":
  print("STARTING")
  print("ESTABLISHING DATABASE CONNECTION")
  conn = db.create_connection('ports.db')

  round_start = datetime.now()
  round_end = round_start + timedelta(0, 60)

  print("STARTING ROUND")
  insert_round_query = """INSERT INTO rounds(start_time) values (?)"""
  db.insert(conn, insert_round_query, (str(round_start.isoformat()),))

  select_round_query = """SELECT id FROM rounds WHERE start_time = ?"""
  current_round = db.select(conn, select_round_query, (str(round_start.isoformat()),))[0][0]

  thread1 = ScannerThread(conn, current_round, round_end)
  thread2 = SnifferThread(conn, current_round, round_end)

  thread1.start()
  thread2.start()

  thread1.join()
  thread2.join()
