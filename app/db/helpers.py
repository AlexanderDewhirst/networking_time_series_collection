import sqlite3
from services.log import Log

def create_connection(filename):
  conn = None
  try:
    conn = sqlite3.connect(filename, check_same_thread = False)
  except sqlite3.Error as e:
    Log(str(e))
  return conn

def insert(conn, query, params):
  try:
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
  except sqlite3.Error as e:
    Log('[' + query + '] ' + str(e))

def insert_many(conn, query, params):
  try:
    c = conn.cursor()
    c.executemany(query, params)
    conn.commit()
  except sqlite3.Error as e:
    Log('[' + query + '] ' + str(e))

def select(conn, query, params = None):
  try:
    c = conn.cursor()
    if params:
      if "%s" in query:
        c.execute(query % params)
      else:
        c.execute(query, params)
    else:
      c.execute(query)
    conn.commit()
    return c.fetchall()
  except sqlite3.Error as e:
    Log('[' + query + '] ' + str(e))

def delete(conn, query, params = None):
  try:
    c = conn.cursor()
    if params:
      if "%s" in query:
        c.execute(query % params)
      else:
        c.execute(query, params)
    else:
      c.execute(query)
    conn.commit()
  except sqlite3.Error as e:
    Log('[' + query + '] ' + str(e))

def seed(conn):
  query = """INSERT INTO ports(value) values (?)"""
  params = list((str(i),) for i in range(1, 65536))
  insert_many(conn, query, params)

def truncate(conn):
  try:
    c = conn.cursor()
    c.execute("""DELETE FROM rounds;""")
    c.execute("""DELETE FROM ports;""")
    c.execute("""DELETE FROM rounds_ports;""")
    c.execute("""DELETE FROM packets;""")
    c.execute("""DELETE FROM batches_rounds;""")
    c.execute("""DELETE FROM batches;""")
    conn.commit()
  except sqlite3.Error as e:
    Log(str(e))
