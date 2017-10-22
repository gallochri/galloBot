#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3
#

import os
import os.path
import sys

from chatterbot import ChatBot


class GalloChatter(object):
    def __init__(self, lang="english"):
        self.language = lang
        self.chatbot = ChatBot(
            'Gallo',
            logic_adapters=[
                "chatterbot.logic.MathematicalEvaluation",
                "chatterbot.logic.TimeLogicAdapter",
                "chatterbot.logic.BestMatch"
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainers'
        )
        self.instdir = "/home/gallochri/dev/galloBot_env/lib/python3.4/site-packages/chatterbot_corpus/data/" \
                       + self.language + "/"
        self.localdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/lang/" + self.language + "/chatbotcorpus/"

    def train(self):
        if self.checkdirnotempty(self.localdir):
            print(self.localdir)
            self.chatbot.train(
                self.localdir
            )
        elif self.checkdirnotempty(self.instdir):
            print(self.instdir)
            self.chatbot.train(
                self.instdir
            )
        else:
            print("Using standard english corpus")
            self.chatbot.train("chatterbot.corpus.english.greetings")

    def reply(self, phrase=""):
        response = self.chatbot.get_response(phrase)
        return response

    def checkdirnotempty(self, folder=""):
        check = False
        if os.path.isdir(folder):
            entities = os.listdir(folder)
            for entities in entities:
                if os.path.isfile(folder + entities):
                    check = True
                    break
        return check
