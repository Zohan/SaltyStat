__author__ = 'Zohan'
import socket
import re
import sys
import csv
import time
import math
import sqlite3 as lite
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import random

mouse = PyMouse()
keyboard = PyKeyboard()

firstFighter = " "
secondFighter = " "
firstFighterSalt = 1
secondFighterSalt = 1
tier = 'N'
saltyWinner = ' '
winningTeam = ' '
baseSalt = 550
baseTournamentSalt = 1500
currentSalt = 500
currentTournamentSalt = 1500
currentBet = 500
betOn = ' '
betsEnabled = 0
isTournament = 0
irc = 0
con = 'salty'
cur = 'db'

def betRed(amount):
    global betOn
    time.sleep(3)
    mouse.click(550,560)
    keyboard.type_string(str(amount))
    time.sleep(1)
    mouse.click(400,650)
    betOn = 'Red'
    return 1
	
def betBlue(amount):
    global betOn
    time.sleep(3)
    mouse.click(550,560)
    keyboard.type_string(str(amount))
    time.sleep(1)
    mouse.click(400,650)
    betOn = 'Blue'
    return 1    

def betAllInRed():
    global betOn
    time.sleep(3)
    mouse.click(880,710)
    time.sleep(2)
    mouse.click(400,625)
    betOn = 'Red'
    return 1

def betAllInBlue():
    global betOn
    time.sleep(3)
    mouse.click(880,710)
    time.sleep(2)
    mouse.click(640,625)
    betOn = 'Blue'
    return 1

def updateSalt():
    global currentSalt, betOn, winningTeam, firstFighterSalt, secondFighterSalt, currentSalt, baseSalt, currentBet
    firstFighterSalt = float(firstFighterSalt)
    if(isinstance(secondFighterSalt, str)):
        secondFighterSalt = secondFighterSalt.split(" ")
        secondFighterSalt = secondFighterSalt[0]
    secondFighterSalt = float(secondFighterSalt)
    ratio = firstFighterSalt/secondFighterSalt
    print(ratio)
    if winningTeam.find('Red') != -1 and betOn.find('Red') != -1:
        currentSalt = currentSalt + (currentSalt/ratio)
        currentSalt = math.ceil(currentSalt)
        print ("You win! Salt at: " + str(currentSalt))
    elif winningTeam.find('Blue') != -1 and betOn.find('Blue') != -1:
        currentSalt = currentSalt + (currentSalt*ratio)
        currentSalt = math.ceil(currentSalt)
        print ("You win! Salt at: " + str(currentSalt))
    else:
        currentSalt -= currentBet
        if currentSalt <= baseSalt:
            print ("Back to the mines!")
            currentSalt = baseSalt
    return 1

def updateTournamentSalt():
    global currentSalt, betOn, winningTeam, firstFighterSalt, secondFighterSalt, currentTournamentSalt, baseTournamentSalt
    firstFighterSalt = float(firstFighterSalt)
    if(isinstance(secondFighterSalt, str)):
        secondFighterSalt = secondFighterSalt.split(" ")
        secondFighterSalt = secondFighterSalt[0]
    secondFighterSalt = float(secondFighterSalt)
    ratio = firstFighterSalt/secondFighterSalt
    currentSalt -= currentTournamentSalt
    print(ratio)
    if winningTeam.find('Red') != -1 and betOn.find('Red') != -1:
        currentTournamentSalt = currentTournamentSalt + (currentSalt/ratio)
        currentTournamentSalt = math.ceil(currentSalt)
        print ("You win! Tourney Salt at: " + str(currentSalt))
    elif winningTeam.find('Blue') != -1 and betOn.find('Blue') != -1:
        currentTournamentSalt = currentTournamentSalt + (currentSalt*ratio)
        currentTournamentSalt = math.ceil(currentSalt)
        print ("You win! Tourney Salt at: " + str(currentSalt))
    else:
        currentTournamentSalt = baseTournamentSalt
        print ("Back to the mines!")
    currentSalt += currentTournamentSalt
    return 1

def addTournamentSaltToCurrentSalt():
    return 0

def betsOpen(text):
    global firstFighter, secondFighter, tier, currentSalt
    print ("Bets Result " +text)   #print text to console
    stringResult = text.split("Bets are OPEN for ")
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
    try:
        stringResult = text.split("Bets are locked. ")
        stringResult = stringResult[1].split(" - $")
        secondFighterSalt = stringResult[2].replace(',', '')
        secondFighterSalt = secondFighterSalt.rstrip('\r\n')
        stringResult = stringResult[1].split(", ")
        firstFighterSalt = stringResult[0].replace(',', '')
        print("Bets: " + firstFighterSalt + " " + secondFighterSalt)
    except (IndexError):
        pass
    return 1

def setWinner(text):
    global saltyWinner, winningTeam, isTournament
    stringResult = text.split(" wins! Payouts to Team ")
    saltyWinner = stringResult[0]
    stringResult = stringResult[1].split(".")
    winningTeam = stringResult[0].rstrip()
    print(stringResult[0] + " " + stringResult[1])
    #outputToCSV()
    #isTournament = 0
    if isTournament:
        updateTournamentSalt()
    else:
        updateSalt()
    writeToSQLite()
    return 1

def getRecommendedFighter():
    global firstFighter, secondFighter
    firstfighterresults = getFighterStats(firstFighter)
    firstfighterwinratio = getWinRate(firstFighter, firstfighterresults)
    secondfighterresults = getFighterStats(secondFighter)
    secondfighterwinratio = getWinRate(secondFighter, secondfighterresults)
    print("Fight ratio: " + firstfighterwinratio.__float__().__str__() + " vs " + secondfighterwinratio.__str__())
    if firstfighterwinratio > secondfighterwinratio:
        print(firstFighter + " should win")
        return 0
    else:
        print(secondFighter + " should win")
        return 1

def getFighterStats(fighter):
    cur.execute("SELECT * FROM fights WHERE FirstFighter=? OR SecondFighter=?", (fighter, fighter))
    return cur.fetchall()

def getWinRate(fighter, fightlist):
    fighterwins = 0.0
    fighterlosses = 0.0
    fightresults = 0.00
    for row in fightlist:
        if row[6].find(fighter) != -1:
            fighterwins += 1
        else:
            fighterlosses += 1
    print("Fightlist Length for " + fighter + ": " + len(fightlist).__str__())
    #print(fightlist)
    if len(fightlist) == 0:
        print("Nothing There")
        return 0
    else:
        fightresults = fighterwins/(fighterlosses+fighterwins)
        print("Returning results: " + fightresults.__str__() + " " + fighterlosses.__str__() + " " + fighterwins.__str__())
        return fightresults

def getSmartBet(fighter):
    fightlist = getFighterStats(fighter)
    smartbet = 0
    fightcount = 0
    print (len(fightlist).__str__())
    for row in fightlist:
        fightcount += 1
        if row[1].find(fighter) != -1:
            smartbet += row[3]/row[4]
        else:
            smartbet += row[4]/row[3]
    if fightcount == 0:
        fightcount = 1
    smartbet = smartbet/fightcount
    print ("Avg odds are : " + smartbet.__str__())
    if smartbet > 1.2:
        smartbet = currentSalt * (1-(1/smartbet))
    elif smartbet < 0.8:
        smartbet = currentSalt*smartbet
    else:
        smartbet = 0.5
    return smartbet


def setAuthor(text):
    #regexResult = re.search('(?<=abc)def', text)
    #print(regexResult.group(0))
    return 1

def setTier(text):
    global tier
    stringResult = text.split()
    tier = stringResult[0]
    print("Tier: " + stringResult[0])
    return 1

def writeToSQLite():
    global firstFighter, firstFighterSalt, secondFighter, secondFighterSalt, tier, saltyWinner, winningTeam, con, cur
    date = time.strftime("%y-%m-%d")
    cur.execute("INSERT INTO Fights(FirstFighter, SecondFighter, FirstFighterSalt, SecondFighterSalt, Tier, SaltyWinner, WinningTeam, Date) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (firstFighter, secondFighter, firstFighterSalt, secondFighterSalt, tier, saltyWinner, winningTeam, date))
    con.commit()

#SQLite
def setup():
    global irc, con, cur
    con = lite.connect('saltybet.db')
    
    with con:
    
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
    
        data = cur.fetchone()
    
        print ("SQLite version: %s" % data)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Fights(ID INTEGER PRIMARY KEY AUTOINCREMENT, FirstFighter TEXT, SecondFighter TEXT, "
                    "FirstFighterSalt INT, SecondFighterSalt INT, Tier TEXT, SaltyWinner TEXT, WinningTeam TEXT, Date DATE)")
        cur.execute("CREATE TABLE IF NOT EXISTS Fighters(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Wins INT, "
                    "Losses INT, ELO INT, Tier TEXT)")
    
    server = "irc.twitch.tv"       #settings
    channel = "#saltybet"
    
    # Enter your username and password here
    botnick = ""
    password = ""

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    
    print ("SaltyStat V 0.33")
    irc.connect((server, 6667)) #connects to the server
    sendMessage = "PASS "+ password +"\n"
    irc.send(sendMessage.encode())    #auth
    sendMessage = "USER "+ botnick +"\n"
    irc.send(sendMessage.encode()) #user authentication
    sendMessage = "NICK "+ botnick +"\n"
    irc.send(sendMessage.encode())      #sets nick
    sendMessage = "JOIN "+ channel +"\n"
    irc.send(sendMessage.encode())       #join the chan
    
    random.seed(time.time())
    
    print ("Looks like we connected...")
    
def mainLoop():
    global irc, con, cur, isTournament, currentSalt, baseTournamentSalt, firstFighter, secondFighter, currentBet
    while 1:    #puts it in a loop
       text = irc.recv(1024)
       try:
           decodedText = text.decode('utf-8')
       except (UnicodeDecodeError):
           pass
       if decodedText.find('PING') != -1:                          #check if 'PING' is found
           sendMessage = 'PONG ' + decodedText.split() [1] + '\r\n'
           irc.send(sendMessage.encode()) #returnes 'PONG' back to the server (prevents pinging out!)
       elif decodedText.find(':waifu4u!waifu4u@waifu4u') != -1:
           waifuTalk = decodedText.partition("#saltybet :")
           waifuTalk = waifuTalk[2]
           #waifuOutput = str(waifuTalk, 'utf-8')
           print ("Waifu talkin")   #print text to console
           if waifuTalk.find('tournament bracket') != -1:
               if isTournament == 0:
                   currentSalt += baseTournamentSalt
               print("We are in a tournament")
               isTournament = 1
           elif waifuTalk.find('next tournament') != -1 or waifuTalk.find('exhibition') != -1:
               isTournament = 0
               #currentSalt += currentTourneySalt
           if waifuTalk.find('Bets are OPEN for ') != -1:
               betsOpen(waifuTalk)
               if isTournament == 1:
                   currentBet = currentTournamentSalt
                   if getRecommendedFighter() == 0:
                       betAllInRed()
                       currentBet = currentSalt
                       print("Betting Red")
                   else:
                       betAllInBlue()
                       print("Betting Blue")
               elif currentSalt < 75000 and betsEnabled == 1:
                   currentBet = currentSalt
                   if getRecommendedFighter() == 1:
                       betAllInRed()
                       print("Betting Red")
                   else:
                       betAllInBlue()
                       print("Betting Blue")
               elif currentSalt > 75000 and betsEnabled == 1:
                   smartbet = 0
                   if getRecommendedFighter() == 0:
                       smartbet = getSmartBet(firstFighter)
                       betRed(smartbet)
                   else:
                       smartbet = getSmartBet(secondFighter)
                       betBlue(smartbet)
                   print("Smartbet is: " + smartbet.__str__())
                   currentBet = smartbet

           elif waifuTalk.find('Bets are locked') != -1:
               betsLocked(waifuTalk)
           elif waifuTalk.find('wins!') != -1:
               setWinner(waifuTalk)
           elif waifuTalk.find('by') == 2:
               setAuthor(waifuTalk)
           elif waifuTalk.find('Tier') != -1:
               setTier(waifuTalk)
           elif waifuTalk.find('next tournament') != -1:
               isTournament = 0
               #currentSalt += currentTourneySalt

       #else:
           #print (decodedText)
               

#setup()
#mainLoop()
