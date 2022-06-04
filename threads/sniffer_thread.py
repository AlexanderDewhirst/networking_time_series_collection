import threading
from helpers import db
from services.ports.sniffer import Sniffer

class SnifferThread(threading.Thread):
  def __init__(self, conn, current_round, round_end):
    threading.Thread.__init__(self)
    self.conn = conn
    self.current_round = current_round
    self.round_end = round_end

  def run(self):
    print("Thread2 start")

    packets = Sniffer(self.round_end)()
    print(packets[0])

    packet_params = []
    for packet in packets:
      protocols = ','.join(packet['protocols'])
      # if packet['srcport'] == None:
      #   print(packet)
      packet_params.append((
        packet['timestamp'],
        protocols,
        packet['qry_name'],
        packet['resp_name'],
        packet['srcport'],
        packet['dstport'],
        packet['payload'],
        self.current_round,
      ))

    insert_packets_query = """
      INSERT INTO packets(
        timestamp, protocols, qry_name, resp_name,
        port_id, dest_port, payload, round_id
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.insert_many(self.conn, insert_packets_query, packet_params)

    print("Thread2 end")
