# Author : Edward Manapov
# Date : 16/01/2015
# Python 3.4

import socket, select
import random
import re
import ssl

def within(value,goal,n):
    if abs(value-goal) < n:
        ok = True
    else:
        ok=False
    return ok

open_sockets = []


listening_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

listening_socket2 = socket.socket( socket.AF_INET, socket.SOCK_STREAM )


listening_socket.bind( ("127.0.0.1", 4000) )
listening_socket2.bind( ("127.0.0.1", 4001) )


listening_socket.listen(5)
listening_socket2.listen(5)

class Client:
        ip = ""
        port = 0
        number = 0
        guesses = 0

connected_clients={}

while True:
    rlist, wlist, xlist = select.select( [listening_socket,listening_socket2] + open_sockets, [], [] )
    for i in rlist:
        if i is listening_socket2:
            new_socket, addr = listening_socket2.accept()
            print ("connection from", addr)
            connstream = ssl.wrap_socket(new_socket,
                    server_side=True,
		    certfile="certs/server.crt",
		    keyfile="certs/server.key",
		    ca_certs="certs/rootCA.crt",
		    cert_reqs=ssl.CERT_REQUIRED)
            open_sockets.append(connstream)
            aclient_response = connstream.recv(1024).decode("utf-8")
            if aclient_response == "Hello":
                connstream.send(bytes("Admin-Greetings", "utf-8"))
            
        elif i is listening_socket:
            new_socket, addr = listening_socket.accept()
            open_sockets.append(new_socket)
            client_response = new_socket.recv(1024).decode("utf-8")
            if client_response == "Hello\r\n":
                new_socket.send(bytes("Greetings\r\n", "utf-8"))
            print ("connection from", addr)
            
                   
            if not (addr[0]+"-"+str(addr[1])) in connected_clients:
                connected_clients[addr[0]+"-"+str(addr[1])]=Client()
                connected_clients[addr[0]+"-"+str(addr[1])].ip = addr[0]
                connected_clients[addr[0]+"-"+str(addr[1])].port = addr[1]
                connected_clients[addr[0]+"-"+str(addr[1])].number = random.randrange(0,21,1)
                connected_clients[addr[0]+"-"+str(addr[1])].guesses = 1

                print ("random number for this client is", connected_clients[addr[0]+"-"+str(addr[1])].number)
            
        else:
                if i.getsockname()[1] == 4001:
                    
                    data = connstream.recv(1024).decode("utf-8")

                    if data == " ":
                        print ("Connection closed with", i.getpeername())
                        connstream.shutdown(socket.SHUT_RDWR)
                        connstream.close()
                        open_sockets.remove(i)                                
                        i.close()
                        break;
                        
                    elif data == "Who":
                        zzz = ""
                        for x in connected_clients:
                            zzz += str(connected_clients[x].ip) + " " + str(connected_clients[x].port) + "\n"
                        msg = "The players currently playing are:\n" + zzz
                        
                        connstream.send(bytes(msg,"utf-8"))
                        connstream.shutdown(socket.SHUT_RDWR)
                        connstream.close()
                        open_sockets.remove(i)
                           
                    else:
                            connstream.send(bytes("Give your command:","utf-8"))

                elif i.getsockname()[1] == 4000:
                    
                    
                    data = i.recv(1024).decode("utf-8")                    
                   
                    if data == " ":
                                print ("Connection closed with", i.getpeername())
                                del connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])]
                                i.close()
                                open_sockets.remove(i)
                                
                    else:
                                
                      
                        x=int(data)
                        

                        if not(within(x,connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].number,1)):
                            if not(within(x,connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].number,3)): 
                                i.send(bytes("Far\r\n","utf-8"))
                            else:
                                i.send(bytes("Close\r\n","utf-8"))
                                                       
                            print ("client",
                                   connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].ip ,
                                   connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].port ,
                                   "gave number" ,
                                   x ,
                                   "but number was",
                                   connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].number)
                            connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].guesses += 1


                        else:
                            i.send(bytes("Correct\r\n","utf-8"))
                            print ("client tried", connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].guesses ,"times to guess the number")
                            print ("Connection closed with", connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].ip , connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])].port)
                            del connected_clients[i.getpeername()[0]+"-"+str(i.getpeername()[1])]
                            open_sockets.remove(i)                            
                            i.close()
                            
