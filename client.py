import socket
import threading
import re
from tkinter import *
from tkinter import ttk

#Send messages to server
def send(msg):
    #Check if Server and client are connected before trying to send a message
    try:
        if(len(msg)!=0):    #If message is empty
            client.send(msg.encode())
            msgList.insert(END,f"\n[192.168.56.1](You): {msg}")     #Print message on GUI
            msgInput.delete(0,END)                                  #Clear the input bar on GUI
    except:
        connectionStatus.set("Disconnected")                        #Server and client disconnected
    return

#Receive messages from server
def receive(addr):
    print(addr)
    ip,port=addr            #Ip and Port of Server
    while True:
        msg=client.recv(2048).decode()
        if not msg:                     #If Server Disconnects
            break
        print(f"{addr}: {msg}")
        if(msg=='diss'):                #If Server Disconnects
            break
        msgList.insert(END,f"\n[{ip}:{port}]: {msg}")       #print Message on GUI
    client.close()
    return
def main(server):
    try:
        serverIp,serverPort=re.split(':',server)        #Extract Ip and Port portion from User Input
    except:
        connectionStatus.set("Invalid IP format. Your IP should follow the syntax in the example above")
        return
    addr=(serverIp,int(serverPort))
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect(addr)
        connectionStatus.set("Connected")
        receive(addr)
    except:
        connectionStatus.set("No Port open on the specified Ip Address and Port")
    return
def start(port):
    mainThread=threading.Thread(target=main,args=(port,))       #New Thread to deal with client-Server communication
    mainThread.start()
    return

def endConnection():
    try:
        client.send("diss".encode())
        connectionStatus.set("Disconnected")
    except:
        connectionStatus.set("Disconnected")
    return
def close():
    root.destroy()      #Close Window

root=Tk()
root.title("Instant LAN messenger chat APP")
mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe,text="Enter Ip and port:  Example(192.168.66.1:5000)").pack()
connectionStatus=StringVar()
connectionStatus.set("Disconnected")
ttk.Label(mainframe,textvariable=connectionStatus).pack()
ip=StringVar()
ipEntry=ttk.Entry(mainframe,width=30,textvariable=ip)
ipEntry.pack()
ipEntry.bind('<Return>',lambda event: start(ip.get()))
ttk.Button(mainframe,text="Connect",command=lambda:start(ip.get())).pack()
msgList = Text(mainframe, height=20,width=50)
msgList.pack()
msg=StringVar()
ttk.Label(mainframe,text="Enter your message:  ").pack()
msgInput=ttk.Entry(mainframe,width=50,textvariable=msg)
msgInput.pack()
msgInput.bind("<Return>",lambda event:send(msg.get()))
ttk.Button(mainframe,text="Send",command=lambda:send(msg.get())).pack()
ttk.Button(mainframe,text="Close",command=close).pack(side=RIGHT)
ttk.Button(mainframe,text="Disconnect",command=endConnection).pack(side=LEFT)
root.mainloop()
