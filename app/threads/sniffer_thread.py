import threading
from db import helpers as db
from services.ports.sniffer import Sniffer

class SnifferThread(threading.Thread):
  def __init__(self, conn, current_round, round_end):
    threading.Thread.__init__(self)
    self.conn = conn
    self.current_round = current_round
    self.round_end = round_end

  def run(self):
    packets = Sniffer(self.round_end)()

    packet_params = []
    for packet in packets:
      if packet['srcport'] != None:
        protocols = ','.join(packet['protocols'])
        packet_params.append((
          protocols,
          packet['timestamp'],
          packet['qry_name'],
          packet['resp_name'],
          packet['srcport'],
          packet['dstport'],
          packet['payload'],
          self.current_round,
        ))

    # TODO: Handle structg corresponding to round data
    #   BatchService - PUT /projects/{id}/rounds/{id}
    insert_packets_query = """
      INSERT INTO packets(
        timestamp, protocols, qry_name, resp_name,
        port_id, dest_port, payload, round_id
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.insert_many(self.conn, insert_packets_query, packet_params)
