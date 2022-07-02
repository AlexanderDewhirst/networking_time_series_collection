import argparse
from db import helpers as db
from services.collect import Collect

parser = argparse.ArgumentParser(description = "Client - Collector component")
parser.add_argument('-d', '--database', dest = 'database', action = 'store', type = str, help = "Database URL")
parser.add_argument('-r', '--round_duration', dest = 'round_duration', action = 'store', default = 60, type = int, help = 'Duration of round.')
parser.add_argument('-p', '--packets', dest = 'packets', action = 'store_true', help = 'Collect packets using Wireshark?')

args = parser.parse_args()

if __name__ == "__main__":
  conn = db.create_connection(args.database)
  Collect(conn, args.round_duration, args.packets)()
