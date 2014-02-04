__author__ = 'Zohan'
import socket
import re

def betsOpen(text):
    regexResult = re.search('(?<=Bets are OPEN for)', text)
    print("Regex:" +regexResult.group(0));
    return 1

def betsLocked(text):
    regexResult = re.search('(?<=Bets are locked.)', text)
    print(regexResult.group(0));
    return 1

def winner(text):
    regexResult = re.search('(?<=wins!)', text)
    print(regexResult.group(0));
    return 1

def author(text):
    regexResult = re.search('(?<=abc)def', text)
    print(regexResult.group(0));
    return 1

server = "irc.twitch.tv"       #settings
channel = "#saltybet"
botnick = "OldSaltySeamon"
password = "oauth:da8xxxzgdevh2m32is0tykln28p8pbb"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

print ("SaltyStat V 0.02")
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
       waifuTalk = decodedText.partition("#saltybet :")
       waifuTalk = waifuTalk[2]
       print ("WAIFU SAYS: " +waifuTalk)   #print text to console
       if waifuTalk.find('Bets are OPEN') != -1:
           betsOpen(waifuTalk)
       elif waifuTalk.find('Bets are locked') != -1:
           betsLocked(waifuTalk)
       elif waifuTalk.find('wins!') != -1:
           winner(waifuTalk)
       elif waifuTalk.find('by') == 2:
           author(waifuTalk)
       elif waifuTalk.find('Bets are locked') != -1:
           betsOpen(waifuTalk)