__author__ = 'Zohan'
import socket
import sys
import string

server = "irc.twitch.tv"       #settings
channel = "#saltybet"
botnick = "OldSaltySeamon"
password = "oauth:da8xxxzgdevh2m32is0tykln28p8pbb"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

print ("SaltyStat V 0.1")
irc.connect((server, 6667))                                                         #connects to the server
sendMessage = "PASS "+ password +"\n"
irc.send(sendMessage.encode())    #auth
sendMessage = "USER "+ botnick +"\n"
irc.send(sendMessage.encode()) #user authentication
sendMessage = "NICK "+ botnick +"\n"
irc.send(sendMessage.encode())      #sets nick
sendMessage = "JOIN "+ channel +"\n"
irc.send(sendMessage.encode())       #join the chan

print ("Looks like we connected...")

while 1:    #puts it in a loop
   text = irc.recv(2048)
   decodedText = text.decode()

   if decodedText.find('PING') != -1:                          #check if 'PING' is found
       sendMessage = 'PONG ' + decodedText.split() [1] + '\r\n'
       irc.send(sendMessage.encode()) #returnes 'PONG' back to the server (prevents pinging out!)
   elif decodedText.find(':waifu4u!waifu4u@waifu4u') != -1:
       saltyLocation = decodedText.partition("#saltybet :")
       print ("WAIFU SAYS: " +saltyLocation[2])   #print text to console
   #else :
       #print(decodedText); # DO NOTHING