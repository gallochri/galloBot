#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3.5
#


import time
import random
import datetime
import telepot
import os
import sys
import subprocess
from gallochatter import GalloChatter

telegramtoken = ''  # telegram bot token from BotFather
checkuserid = 1  # enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv'  # the file where we store the list of users who can talk with bot
attemptsfile = '/tmp/attempts.log'  # the file where we log denied accesses
active = 1  # if set to 0 the bot will stop

language = "it-IT"

chatter = GalloChatter(language)
chatter.train()

if telegramtoken == '' and os.path.isfile("telegramtoken.txt"):
    text_file = open("telegramtoken.txt", "r")
    telegramtoken = text_file.read().replace("\n", "")
    text_file.close()

print("Connecting to Telegram...")
bot = telepot.Bot(telegramtoken)
print(bot.getMe())


def listusers():
    if not os.path.isfile(usersfile):
        return ''
    text_file = open(usersfile, "r")
    lines = text_file.read().split(',')
    text_file.close()
    del lines[-1]  # remove last element since it is blank
    return lines


def adduser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            csv = csv + usr + ","
    csv = csv + name + ","
    text_file = open(usersfile, "w")
    text_file.write(csv)
    text_file.close()


def deluser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            if usr != name:
                csv = csv + usr + ","
    text_file = open(usersfile, "w")
    text_file.write(csv)
    text_file.close()


def handle(msg):
    global bot
    global chatter
    global language

    chat_id = msg['chat']['id']
    sender = msg['from']['id']

    users = listusers()

    if checkuserid == 1:
        verified = 0
        if users != "":
            for usr in users:
                if str(sender) == usr:
                    verified = 1
        if verified == 0:
            bot.sendMessage(chat_id, "I don't talk with strangers, dear " + str(sender))
            # write this user in the list of attempted accesses
            if attemptsfile != '':
                lines = ''
                if os.path.isfile(attemptsfile):
                    text_file = open(attemptsfile, "r")
                    lines = text_file.read()
                    text_file.close()
                lines = lines + str(datetime.datetime.now()) + " --- UserdID: " + str(sender) + " DENIED \n"
                text_file = open(attemptsfile, "w")
                text_file.write(lines)
                text_file.close()
            return

    command = ''

    try:
        if msg['text'] != '':
            command = msg['text']
            print('Got command: ' + command)
    except:
        print("No text in this message")

    if command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif '/adduser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
            adduser(usrname)
            bot.sendMessage(chat_id, "User " + usrname + " added")
    elif '/deluser' in command:
        if len(command.split(' ')) > 1:
            usrname = command.split(' ')[1]
            deluser(usrname)
            bot.sendMessage(chat_id, "User " + usrname + " deleted")
    elif command == '/help':
        bot.sendMessage(chat_id, "/adduser /deluser /time /exit")
    elif command == '/exit':
        global active
        active = False
        bot.sendMessage(chat_id, "The bot will shutdown in 10 seconds")
    elif command != '':
        answer = chatter.reply(command)
        bot.sendMessage(chat_id, str(answer))


bot.message_loop(handle)
print('I am listening ...')

while active:
    time.sleep(10)
print("Exiting")
sys.exit()
