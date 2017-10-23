#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3.5
#


import datetime
import sys
import time

import os
import telepot

from gallochatter import GalloChatter

telegramtoken = ''  # telegram bot token from BotFather
checkuserid = 1  # enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv'  # the file where we store the list of users who can talk with bot
attemptsfile = '/tmp/attempts.log'  # the file where we log denied accesses
active = 1  # if set to 0 the bot will stop

language = "italian"

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
    auth_file = open(usersfile, "r")
    lines = auth_file.read().split(',')
    auth_file.close()
    del lines[-1]  # remove last element since it is blank
    return lines


def adduser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            csv = csv + usr + ","
    csv = csv + name + ","
    auth_file = open(usersfile, "w")
    auth_file.write(csv)
    auth_file.close()


def deluser(name):
    csv = ""
    users = listusers()
    if users != "":
        for usr in users:
            if usr != name:
                csv = csv + usr + ","
    auth_file = open(usersfile, "w")
    auth_file.write(csv)
    auth_file.close()


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
                    auth_file = open(attemptsfile, "r")
                    lines = auth_file.read()
                    auth_file.close()
                lines = lines + str(datetime.datetime.now()) + " --- UserdID: " + str(sender) + " DENIED \n"
                auth_file = open(attemptsfile, "w")
                auth_file.write(lines)
                auth_file.close()
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
            username = command.split(' ')[1]
            adduser(username)
            bot.sendMessage(chat_id, "User " + username + " added")
    elif '/deluser' in command:
        if len(command.split(' ')) > 1:
            username = command.split(' ')[1]
            deluser(username)
            bot.sendMessage(chat_id, "User " + username + " deleted")
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
