import dotenv
from db import helpers as db
from services.detect import Detect

dotenv.load_dotenv()

if __name__ == "__main__":
  conn = db.create_connection('/Users/alexanderdewhirst/ports.db')

  detector = Detect(conn)
  detector()
