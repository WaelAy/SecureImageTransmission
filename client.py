import socket
import threading
import time
import os
from DH import DH
from cryptography.hazmat.backends import default_backend

HEADER = 2048
FORMAT = "UTF-8"
SERVER = "192.168.1.102"
PORT = 5555
DISCONNEC_MSG = "#DISCONNECT"
ADDR = (SERVER,PORT)
RECV = False
client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_state = False

image_num = 1



def set_state(state:bool):
    global client_state 
    client_state = state

def get_state():
    return client_state

def start():
    while not get_state():
        try:
            client.connect(ADDR)
            
        except Exception as Error:
            print(f"[{socket.gethostname()}]Error couldn't connect to server {Error}")
            time.sleep(5)

        else:
            set_state(True)
            print(f"[{socket.gethostname()}]Server {SERVER} connected successfully!")

def send(msg):
    try:
        message = msg.encode(FORMAT)
        #msg_length = len(message)
        #send_length = str(msg_length).encode(FORMAT)
        #send_length += b' ' * (HEADER - len(send_length))
        #client.send(send_length)
        client.send(message)
    except  Exception as Error:
        print(f"[client]Error couldn't send to server! {Error}")
        client.close()
        set_state(False)
        time.sleep(5)


        

def recieve():
    while True:
        try:
            if get_state():
                MSG = client.recv(2048).decode(FORMAT)
                if MSG:
                    print(f"[Client:{client.getsockname()[0]}]{MSG}")
                if MSG.strip() == DISCONNEC_MSG:
                    client.close()
                    print(f"[{socket.gethostname()}] Server Disconnected!")

        except:
            print(f"[{socket.gethostname()}]Error Couldn't recieve from server")
            time.sleep(5)
            set_state(False)
            

def recv_img():
        global image_num
        try:   
            image_chunk = client.recv(HEADER)
            client.settimeout(2)
            file = open(f"compressed_image{image_num}.jpeg","wb")
            image_num+=1
            x = 0
        
            if image_chunk:
                while image_chunk:
                    file.write(image_chunk)
                    try:
                        image_chunk = client.recv(HEADER)
                    except:
                        break
                    x+=1

                file.close()
                print("Image recieved!")
        except:
            pass
        
 

def recv_key():
    while True:
        x = int(client.recv(HEADER))
        print(x)
        if (x):
            break


start()




x =threading.Thread(target=recieve)

x.start()


while True:
    if not get_state():
        start()
    
        #message = input()
        #send(message)

   
    