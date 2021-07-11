import scapy.all as scapy
import argparse as op

def output(answered):
    result = {}
    print('\tIP ADDRESS\t |\tMAC ADDRESS')
    print(('-'*25) + "|" + ('-'*25))
    for element in answered:
        result[element[1].psrc] = element[1].hwsrc
    '''
        psrc = IP ADDRESS OF SOURCE
        hwsrc = MAC ADDRESS OF SOURCE 
    '''
    for ip, mac in result.items():
        print(f"\t{ip}\t ",end = '|')
        print(f"\t{mac}\t")

def scan(ip):
    #scapy.ls(scapy.ARP())       #THIS FUNCTION IS USED TO FIND A MODULE INSIDE A CLASS
    arp_request = scapy.ARP(pdst = ip)  #pdst IS A MODULE IN ARP() CLASS
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_result = broadcast/arp_request
    #arp_result.show()
    '''
    show detailed result of arp_result, print(arp_result.summary()) is used for short results
    '''

    output(answered= scapy.srp(arp_result,timeout = 1, verbose = False)[0])
    '''
    SEND RECIVE PACKETS(.srp) IS USED TO OBTAIN MAC ADDRESSES ACROSS THE IP RANGE IN FORM OF A LIST
    timeout IS USED TO SET THE TIME DURATION TO SEND PACKETS OVER AN IP
    verbose is used to eliminate scrapy.srp output
    '''

def ip():
    parser = op.ArgumentParser()
    parser.add_argument("-t","--target", dest = "ip", help = "Enter the IP address.")
    options,arguments = parser.parse_args()
    return options.ip


scan(ip())
