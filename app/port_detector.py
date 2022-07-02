import dotenv
from db import helpers as db
from services.detect import Detect

dotenv.load_dotenv()

## Use argparse
# - database, --d
#   '/Users/alexanderdewhirst/ports.db'
# - model, --m
#   CnnLstmAe
# - num_rounds_per_batch, --n
#   60
#

if __name__ == "__main__":
  conn = db.create_connection('/Users/alexanderdewhirst/ports.db')

  Detect(conn)()
