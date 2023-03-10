import socket
import threading
from tkinter import *
from tkinter import ttk

activeConnections=[]            #List of all clients connected to the server
def handleClient(conn,addr):
    print(addr)
    ip,port=addr
    while True:
        msg=conn.recv(2048).decode()
        if not msg:
            break
        print(f"{ip}: {msg}")
        if(msg=='diss'):
            break
        msgList.insert(END,f"\n[{ip}:{port}]: {msg}")
    activeConnections.remove(conn)          #Remove client from List
    conn.close()                            #Close Connection
    return
def respond(msg):
    msgList.insert(END,f"\n[192.168.56.1](You): {msg}")
    msgInput.delete(0,END)
    for c in activeConnections:
        c.send(msg.encode())
    return
def main(port):
    ip=socket.gethostbyname(socket.gethostname())
    print(ip)
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.settimeout(1)                    #To make server timeout after every 1 second to make it non blocking
    server.bind((ip,port))
    server.listen()
    print("server started")
    while True:
        try:
            conn,addr=server.accept()
            activeConnections.append(conn)
            thread=threading.Thread(target=handleClient,args=(conn,addr))
            thread.start()
        except socket.timeout:                  #Check for keyboard interrupts else continue listening
            continue
    server.close()
def start(port):
    mainThread=threading.Thread(target=main,args=(port,),daemon=True)       #Thread for listening
    mainThread.start()
    return

def close():
    root.destroy()

#Main thread for GUI
root=Tk()
root.title("Instant LAN messenger chat APP")
mainframe=ttk.Frame(root,padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(mainframe,text="Enter Port to listen on: ").pack()
ip=IntVar()
ipEntry=ttk.Entry(mainframe,width=10,textvariable=ip)
ipEntry.pack()
ipEntry.bind('<Return>',lambda event: start(ip.get()))
#Call to Function Start to start Thread for listening
ttk.Button(mainframe,text="Connect",command=lambda:start(ip.get())).pack()
msgList = Text(mainframe, height=20,width=50)
msgList.pack()
msg=StringVar()
ttk.Label(mainframe,text="Enter your message:  ").pack()
msgInput=ttk.Entry(mainframe,width=50,textvariable=msg)
msgInput.pack()
msgInput.bind("<Return>",lambda event:respond(msg.get()))
ttk.Button(mainframe,text="Send",command=lambda:respond(msg.get())).pack()
ttk.Button(mainframe,text="Close",command=close).pack(side=RIGHT)
root.mainloop()


