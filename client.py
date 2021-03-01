import socket
import threading

HOST = '127.0.0.1'
PORT = 10000


class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.nickname = input("Please choose a nickname: ")

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def gui_loop(self):
        print(f"Your nickname: {self.nickname}\n")
        while True:
            self.write()
        self.gui_done = True

    def write(self):
        message = input()
        self.sock.send(f"{self.nickname}: {message}".encode('utf-8'))

    def stop(self):
        self.running = False
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                message = message.decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)