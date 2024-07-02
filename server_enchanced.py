import socket
import threading
import time
from DH import *

from cryptography.hazmat.backends import default_backend

class Server():


    def __init__(self):
        self.port = 5555
        self.ip_address = "192.168.1.102" #socket.gethostbyname(socket.gethostname())
        self.name = socket.gethostname()
        self.format = "UTF-8"
        self.disconnect_msg = "#DIS"
        self.address = (self.ip_address,self.port)
        self.header = 2048
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = []
        self.image_num = 0

    def init_Server(self):
        self.server.bind(self.address)
        print(f"[SERVER]Initisializing Server {self.address[0]}")
        self.server.listen()
        print("[Server]Server Initialised Successfully!")
        thread = threading.Thread(target=self.add_client)
        thread.start()
    

    def add_client(self):
        

        while True:
            conn,addrs = self.server.accept()
            if conn not in self.clients:
                self.clients.append(conn)
                print(f"[SERVER] {self.clients.__len__()} Active Connections.")
                threading.Thread(target=self.recieve_msg,args=[conn]).start()
            

    def recieve_msg(self,conn:socket.socket):

        while True:
            try:
                    if (conn):
                        msg_length = conn.recv(self.header).decode(self.format)
            
                        if msg_length:
                            #msg_length = int(msg_length)
                            #msg = self.clients[0].recv(msg_length.__len__()).decode(self.format)
                            #msg = self.clients[0].recv(self.header).decode(self.format)
                            print(f"[Client:{conn.getsockname()[0]}] {msg_length}")

            except Exception as err:
                print(f"[SERVER]Error Client[{conn.getsockname()[0]}] Connection lost ending socket in 5s....")
                
                try:
                        conn.close()
                        self.clients.remove(conn)
                        break
                except Exception as ERR:
                        print(ERR)
                        

        time.sleep(5)


    def send_message(self,socket:int,msg:str):
            try:
                msg.encode(self.format)
                msg_length = len(msg)
                send_length = str(msg_length).encode(self.format)
                send_length += b' ' * (self.header - len(send_length))               
                self.clients[socket].send(msg.encode(self.format))
            except Exception as err:
                print(f"[SERVER]Error happened couldn't send message!")


    def send_img(self,path:str,client_num:int):
        try:
            try:
                file = open(f"{path}","rb")
                image_chunk = file.read(self.header)

            except:
                print("[SERVER]Couldn't read file please try again!")

            if image_chunk:
                print("[SERVER]Sending image....")

            try:
                while image_chunk:
                    self.clients[client_num].send(image_chunk)
                    image_chunk = file.read(self.header)
                    
                self.clients[client_num].send("IMAGE_DONE".encode(self.format))
                print("[SERVEER]Transmission complete.")

                file.close()
            except:
                print(f"[SERVER]Error Couldn't send image to client:{client_num}")
        except:
            print("[SERVER]Error couldn't send file!")
            print("[SERVER]Please Try again in 5s")
            time.sleep(5)
        
    def exchange_key(self,client:int,params:int):
        key = 0
        while True:
            self.clients[client].send(str(params))
            ack_msg = self.clients[client].recv()
            if ack_msg == "ACK_PARAMS":
                client_pk = self.clients[client].recv(self.header)
                key = client_pk
                break
        
        return int(key)
    


s = Server()
s.init_Server()




while True:
    
    
    
    #priv_k,pub_k = generate_dh_key_pair(params)
    #bytez = pub_k.public_numbers().y.to_bytes(2048,'big')
    #dh.DHParameterNumbers()
    #x = input()
    
    s.send_message(0,"hello")
    time.sleep(5)
    #s.send_img(x.strip(),0)
    

    