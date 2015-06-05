__author__ = 'Zohan'
import socket
import re
import sys
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
    firstFighter = stringResult[0];
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
    secondFighterSalt = stringResult[2].replace(',', '')
    secondFighterSalt = secondFighterSalt.rstrip('\r\n')
    stringResult = stringResult[1].split(", ")
    firstFighterSalt = stringResult[0].replace(',', '')
    print("Bets: " + firstFighterSalt + " " + secondFighterSalt)
    return 1

def setWinner(text):
    global saltyWinner, winningTeam
    stringResult = text.split(" wins! Payouts to Team ");
    saltyWinner = stringResult[0]
    winningTeam = stringResult[1].rstrip()
    print(stringResult[0] + " " + stringResult[1])
    outputToCSV()
    return 1

def setAuthor(text):
    #regexResult = re.search('(?<=abc)def', text)
    #print(regexResult.group(0))
    return 1

def setTier(text):
    global tier;
    stringResult = text.split()
    tier = stringResult[0]
    print("Tier: " + stringResult[0])
    return 1

def outputToCSV():
    global firstFighter, firstFighterSalt, secondFighter, secondFighterSalt, tier, saltyWinner, winningTeam
    if tier.find('S') != -1:
        with open("sTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    elif tier.find('A') != -1:
        with open("aTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    elif tier.find('B') != -1:
        with open("bTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    elif tier.find('P') != -1:
        with open("pTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    elif tier.find('NEW') != -1:
        with open("newTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    elif tier.find('X') != -1:
        with open("xTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()
    else:
        with open("shakerTier"+time.strftime("%m-%d-%y")+".csv", 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam])
            csvfile.close()

server = "irc.twitch.tv"       #settings
channel = "#saltybet"
botnick = ""
password = ""
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
   decodedText = text.decode('utf-8')
   if decodedText.find('PING') != -1:                          #check if 'PING' is found
       sendMessage = 'PONG ' + decodedText.split() [1] + '\r\n'
       irc.send(sendMessage.encode()) #returnes 'PONG' back to the server (prevents pinging out!)
   elif decodedText.find(':waifu4u!waifu4u@waifu4u') != -1:
       waifuTalk = decodedText.partition("#saltybet :")
       waifuTalk = waifuTalk[2]
       #waifuOutput = str(waifuTalk, 'utf-8')
       print ("Waifu said things")   #print text to console
       if waifuTalk.find('Bets are OPEN for ') != -1:
           betsOpen(waifuTalk)
       elif waifuTalk.find('Bets are locked') != -1:
           betsLocked(waifuTalk)
       elif waifuTalk.find('wins!') != -1:
           setWinner(waifuTalk)
       elif waifuTalk.find('by') == 2:
           setAuthor(waifuTalk)
       elif waifuTalk.find('Tier') != -1:
           setTier(waifuTalk)