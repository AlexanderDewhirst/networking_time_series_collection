import argparse
from db import helpers as db
from services.cleanup import Cleanup

## Use argparse
# - database, --d
#   '/Users/alexanderdewhirst/ports.db'
#

parser = argparse.ArgumentParser(description = 'Client - Cleanup component')
parser.add_argument('-d', '--database', dest = 'database', action = 'store', type = str, help = 'Database URL')

args = parser.parse_args()

if __name__ == "__main__":
  conn = db.create_connection(args.database)
  Cleanup(conn)()
