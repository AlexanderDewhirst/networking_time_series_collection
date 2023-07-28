import dotenv
import argparse
from db import helpers as db
from services.detect import Detect

dotenv.load_dotenv()

parser = argparse.ArgumentParser(description = "Client - Detector component")
parser.add_argument('-d', '--database', dest = 'database', action = 'store', type = str, help = "Database URL")
parser.add_argument('-r', '--batches_per_round', dest = 'batches_per_round', action = 'store', default = 60, type = int, help = 'Batches per round.')

args = parser.parse_args()

if __name__ == "__main__":
  conn = db.create_connection(args.database)
  Detect(conn, args.batches_per_round)()
