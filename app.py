#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3.5
#


import datetime
import sys
import time
import csv

import os
import telepot

from gallochatter import GalloChatter
import settings

telegramtoken = os.environ.get("bot_token")
language = os.environ.get("language")

# TODO
checkuserid = 1  # enable users whitelist, so only certain people can talk with this bot
usersfile = 'botusers.csv'  # the file where we store the list of users who can talk with bot
attemptsfile = 'attempts.log'  # the file where we log denied accesses
active = 1  # if set to 0 the bot will stop

chatter = GalloChatter(language)
chatter.train()

print("Connecting to Telegram...")
bot = telepot.Bot(telegramtoken)
print(bot.getMe())


def listusers():
    if not os.path.isfile(usersfile):
        return 'No user file'
    with open(usersfile) as csvfile:
        reader = csv.DictReader(csvfile)
        print("Authorized users list:")
        for row in reader:
            print(row['ID'], row['Username'])
    # auth_file = open(usersfile, "r")
    # lines = auth_file.read().split(',')
    # auth_file.close()
    # del lines[-1]  # remove last element since it is blank
    # return lines


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
    sender_id = msg['from']['id']
    sender_first_name = msg['from']['first_name']
    sender_last_name = msg['from']['last_name']

    if checkuserid == 1:
        verified = 0
        with open(usersfile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if str(sender_id) == row['ID']:
                    verified = 1
        if verified == 0:
            bot.sendMessage(chat_id, "I don't talk with strangers, dear " + str(sender_first_name))
            # write this user in the list of attempted accesses
            if attemptsfile != '':
                lines = ''
                if os.path.isfile(attemptsfile):
                    auth_file = open(attemptsfile, "r")
                    lines = auth_file.read()
                    auth_file.close()
                lines = lines + str(datetime.datetime.now()) + " --- User ID: " + str(sender_id) + " Name: " + \
                        str(sender_first_name) + " " + str(sender_last_name) + " DENIED \n"
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
        bot.sendMessage(chat_id, "/listusers /adduser /deluser /time /exit")
    elif command == '/exit':
        global active
        active = False
        bot.sendMessage(chat_id, "The bot will shutdown in 10 seconds")
    elif command == '/listusers':
        listusers()
    elif command != '':
        answer = chatter.reply(command)
        bot.sendMessage(chat_id, str(answer))


bot.message_loop(handle)
print('I am listening ...')

while active:
    time.sleep(10)
print("Exiting")
sys.exit()
