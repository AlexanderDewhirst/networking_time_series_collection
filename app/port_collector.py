from db import helpers as db
from services.collect import Collect

if __name__ == "__main__":
  conn = db.create_connection('ports.db')
  Collect(conn)()