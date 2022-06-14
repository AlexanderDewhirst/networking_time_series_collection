import sqlite3

def create_connection(filename):
  conn = None
  try:
    conn = sqlite3.connect(filename, check_same_thread = False)
  except sqlite3.Error as e:
    print(e)
  return conn

def insert(conn, query, params):
  try:
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
  except sqlite3.Error as e:
    print(e)
    print(query)

def insert_many(conn, query, params):
  try:
    c = conn.cursor()
    c.executemany(query, params)
    conn.commit()
  except sqlite3.Error as e:
    print(e)
    print(query)

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
    print(e)
    print(query)

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
    conn.commit()
  except sqlite3.Error as e:
    print(e)
