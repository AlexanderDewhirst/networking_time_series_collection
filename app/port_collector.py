from db import helpers as db
from services.collect import Collect

## Use argparse
# - database, --d
#   '/Users/alexanderdewhirst/ports.db'
# - round_duration, --r
#   60
# - packets, --p
#   1 (true)
#

if __name__ == "__main__":
  conn = db.create_connection('ports.db')
  Collect(conn)()
