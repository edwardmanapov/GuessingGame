# Author : Edward Manapov
# Date : 16/01/2015
# Python 3.4

import socket

server_response = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4000))

while server_response == False:
    s.send(bytes("Hello\r\n","utf-8"))
    g =s.recv(1024).decode("utf-8")
    if g == "Greetings\r\n":
        x="Welcome to the Guess the Number game!\nWhat is your guess? "
        server_response = True       
while (x):
    r = input(x)  
    s.send(bytes(r,"utf-8"))
    response = s.recv(1024).decode("utf-8")
    if response == "Far\r\n":
        x = "You are way off.\nWhat is your next guess? "
    elif response == "Close\r\n":
        x = "You are close!\nWhat is your next guess? "
    elif response == "Correct\r\n":
        x = "You guessed correctly!"
        break
print (x)
s.close()
