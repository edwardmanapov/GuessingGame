# Author : Edward Manapov
# Date : 16/01/2015
# Python 3.4

import socket
import ssl

server_response = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connstream = ssl.wrap_socket(s,
	certfile="certs/9.crt",
	keyfile="certs/9.key",
	ca_certs="certs/rootCA.crt",
        cert_reqs=ssl.CERT_REQUIRED)

connstream.connect(("127.0.0.1", 4001))

while server_response == False:
    connstream.send(bytes("Hello","utf-8"))
    g =connstream.recv(1024).decode("utf-8")
    if g == "Admin-Greetings":

        server_response = True       

        connstream.send(bytes("Who","utf-8"))
        x = connstream.recv(1024).decode("utf-8")
        print (x)
connstream.close()
