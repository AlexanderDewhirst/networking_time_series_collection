from db import helpers as db
from services.cleanup import Cleanup

## Use argparse
# - database, --d
#   '/Users/alexanderdewhirst/ports.db'
#

if __name__ == "__main__":
  conn = db.create_connection('ports.db')
  Cleanup(conn)()
