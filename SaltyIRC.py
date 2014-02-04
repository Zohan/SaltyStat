__author__ = 'Zohan'
import socket
import re
import csv
import time

firstFighter = ' '
secondFighter = ' '
firstFighterSalt = ' '
secondFighterSalt = ' '
tier = 'N'
saltyWinner = ' '
winningTeam = ' '

def betsOpen(text):
    global firstFighter
    global secondFighter
    global tier
    stringResult = text.split("Bets are OPEN for ");
    stringResult = stringResult[1].split(" vs ")
    firstFighter = stringResult[0]
    stringResult = stringResult[1].split("! (")
    secondFighter = stringResult[0]
    stringResult = stringResult[1].split(" Tier)")
    tier = stringResult[0]
    print("Fighters: " + firstFighter + " vs " + secondFighter + " Tier: " + tier)
    return 1

def betsLocked(text):
    global firstFighterSalt, secondFighterSalt
    stringResult = text.split("Bets are locked. ");
    stringResult = stringResult[1].split(" - $")
    secondFighterSalt = stringResult[2]
    stringResult = stringResult[1].split(", ")
    firstFighterSalt = stringResult[0]
    print("Bets: " + firstFighterSalt + " " + secondFighterSalt )
    return 1

def winner(text):
    global saltyWinner, winningTeam
    stringResult = text.split(" wins! Payouts to Team ");
    saltyWinner = stringResult[0]
    winningTeam = stringResult[1]
    print(stringResult[0] + " " + stringResult[1])
    outputToCSV()
    return 1

def author(text):
    regexResult = re.search('(?<=abc)def', text)
    print(regexResult.group(0))
    return 1

def outputToCSV():
    global firstFighter, firstFighterSalt, secondFighter, secondFighterSalt, tier, saltyWinner, winningTeam
    print("Outputting "+ firstFighter + " vs " + secondFighter + " Tier: " + tier)
    if tier.find('S') != -1:
        with open("sTier"+time.strftime("%m-%d-%y")+".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, winner, winningTeam])
    elif tier.find('A') != -1:
        with open("aTier"+time.strftime("%m-%d-%y")+".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, winner, winningTeam])
    elif tier.find('B') != -1:
        with open("bTier"+time.strftime("%m-%d-%y")+".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, winner, winningTeam])
    elif tier.find('P') != -1:
        with open("pTier"+time.strftime("%m-%d-%y")+".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, winner, winningTeam])

server = "irc.twitch.tv"       #settings
channel = "#saltybet"
botnick = "OldSaltySeamon"
password = "oauth:da8xxxzgdevh2m32is0tykln28p8pbb"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

print ("SaltyStat V 0.2")
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
       if waifuTalk.find('Bets are OPEN for ') != -1:
           betsOpen(waifuTalk)
       elif waifuTalk.find('Bets are locked') != -1:
           betsLocked(waifuTalk)
       elif waifuTalk.find('wins!') != -1:
           winner(waifuTalk)
       elif waifuTalk.find('by') == 2:
           author(waifuTalk)