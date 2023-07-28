import argparse
from services.splitter import Splitter

parser = argparse.ArgumentParser(description = "Client - Splitter component")
parser.add_argument('-f', '--filename', dest = 'file', action = 'store', type = str, help = "File path to split")

args = parser.parse_args()

if __name__ == "__main__":
  Splitter(args.file)()
