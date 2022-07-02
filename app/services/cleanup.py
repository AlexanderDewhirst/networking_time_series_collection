from db import helpers as db
from services.log import Log

class Cleanup():
  def __init__(self, conn):
    self.conn = conn
    self.current_batch = self.__get_current_batch()

  def __call__(self):
    rounds_to_delete = self.__get_stale_rounds()
    rounds_to_delete = str(tuple(map(lambda x: str(x[0]), rounds_to_delete)))

    delete_rounds_ports_query = """DELETE FROM rounds_ports WHERE round_id IN %s;"""
    delete_packets_query = """DELETE FROM packets WHERE round_id IN %s;"""
    delete_batches_rounds_query = """DELETE FROM batches_rounds WHERE round_id IN %s;"""
    delete_rounds_query = """DELETE FROM rounds WHERE id IN %s;"""
    delete_batch_query = """DELETE FROM batches WHERE id != %s;"""

    Log("Deleting stale data - retaining batch " + str(self.current_batch))

    db.delete(self.conn, delete_rounds_ports_query, rounds_to_delete)
    db.delete(self.conn, delete_packets_query, rounds_to_delete)
    db.delete(self.conn, delete_batches_rounds_query, rounds_to_delete)
    db.delete(self.conn, delete_rounds_query, rounds_to_delete)
    db.delete(self.conn, delete_batch_query, self.current_batch)

    Log("Successfully deleted stale data")

  def __get_current_batch(self):
    select_batch_query = """SELECT id FROM batches ORDER BY id DESC LIMIT 1;"""
    return str(db.select(self.conn, select_batch_query)[0][0])

  def __get_stale_rounds(self):
    select_rounds_query = """SELECT round_id FROM batches_rounds WHERE batch_id != ?;"""
    return db.select(self.conn, select_rounds_query, (self.current_batch, ))
