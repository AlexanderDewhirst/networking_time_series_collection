import helpers as db

if __name__ == "__main__":
  conn = db.create_connection('ports.db')
  print("TRUNCATING TABLES")
  db.truncate(conn)
  print("SEEDING DATABASE")
  db.seed(conn)
