import parser
from subprocess import *
from optparse import *
phrase = OptionParser()
phrase.add_option("-i","--interface", dest = "interface", help ="Input interface to change")
phrase.add_option("-m","--mac", dest = "mac", help ="Enter a mac id xx:xx:xx:xx:xx:xx(optional)")
option,arguments = phrase.parse_args()

interface = option.interface
mac = option.mac

if not interface:
    phrase.error("Invalid interface.\nUse --help for more info")
else:
    call(["ifconfig",interface,"down"])

    if not mac:
        call(["macchanger","-a",interface])
    else:
        call(["macchanger","-m",mac,interface])

    call(["ifconfig", interface, "up"])