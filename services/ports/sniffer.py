import pyshark
from datetime import datetime

class Sniffer:
  def __init__(self, end):
    self.interface = 'en0'
    self.ports = []
    self.end = end

  def __call__(self):
    capture = pyshark.LiveCapture(interface=self.interface)

    for packet in capture.sniff_continuously():
      if datetime.now() > self.end:
        break

      packet_info = { 'srcport': None, 'dstport': None, 'qry_name': None, 'resp_name': None, 'payload': None }
      packet_info['protocols'] = []
      packet_info['timestamp'] = packet.sniff_time

      if 'DNS' in packet:
        dns_layer = packet['DNS']
        packet_info['protocols'].append('DNS')
        packet_info['qry_name'] = dns_layer.qry_name
        if dns_layer.flags_response == 1:
          packet_info['resp_name'] = dns_layer.resp_name

      if 'TCP' in packet:
        tcp_layer = packet['TCP']
        packet_info['protocols'].append('TCP')
        packet_info['srcport'] = int(tcp_layer.srcport)
        packet_info['dstport'] = int(tcp_layer.dstport)

      if 'UDP' in packet:
        udp_layer = packet['UDP']
        packet_info['protocols'].append('UDP')
        packet_info['srcport'] = int(udp_layer.srcport)
        packet_info['dstport'] = int(udp_layer.dstport)
        packet_info['payload'] = udp_layer.payload

      if 'QUIC' in packet:
        quic_layer = packet['QUIC']
        packet_info['protocols'].append('QUIC')
        if 'payload' in quic_layer.field_names:
          packet_info['payload'] = quic_layer.payload
        elif 'remaining_payload' in quic_layer.field_names:
          packet_info['payload'] = quic_layer.remaining_payload

      # if packet_info['protocols'] == []:
      #   print(packet)
      else:
        self.ports.append(packet_info)
    return self.ports
