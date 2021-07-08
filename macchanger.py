from subprocess import *
from optparse import *
import re
import random

phrase = OptionParser()
phrase.add_option("-i","--interface", dest = "interface", help ="Input interface to change")
phrase.add_option("-m","--mac", dest = "mac", help ="Enter a mac id xx:xx:xx:xx:xx:xx(optional)")
option,arguments = phrase.parse_args()

def random_mac():
    mac_number = ['0','1','2','3','4','5','6','7','8','9']
    mac_id = ""
    for i in range(1,18):
        if i%3 == 0:
            mac_id+=":"
        else:
            mac_id+=random.choice(mac_number)
    return mac_id

interface = option.interface
mac = option.mac

ifconfig = check_output(["ifconfig",interface]).decode()
old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)


if not interface:
    phrase.error("Invalid interface.\nUse --help for more info")
else:
    if old_mac:
        print(f"Old Mac: {old_mac.group(0)}")
    call(["ifconfig",interface,"down"])

    if not mac:
        mac_id = random_mac()
        call(["ifconfig", interface,"hw","ether",mac_id])
    else:
        call(["ifconfig", interface, "hw", "ether", mac])

    call(["ifconfig", interface, "up"])
    ifconfig = check_output(["ifconfig", interface]).decode()
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    print(f"New Mac: {new_mac.group(0)}")

