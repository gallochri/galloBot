#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Run this code with python3
#

import os
import os.path
import sys
import chatterbot

from chatterbot import ChatBot


class GalloChatter(object):
    def __init__(self, lang="english"):
        self.db_uri = os.environ.get('database_uri')
        self.language = lang
        self.chatbot = ChatBot(
            'Gallo',
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            database_uri=self.db_uri,
            logic_adapters=[
                "chatterbot.logic.MathematicalEvaluation",
                "chatterbot.logic.TimeLogicAdapter",
                "chatterbot.logic.BestMatch"
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )
        self.instdir = os.path.dirname(chatterbot.__file__) + "_corpus/data/" + self.language + "/"
        self.localdir = os.path.abspath(os.path.dirname(sys.argv[0])) + "/lang/" + self.language + "/chatbotcorpus/"

    def train(self):
        print("###Start training###")
        if self.checkdirnotempty(self.localdir):
            self.chatbot.train(self.localdir)
            print("Training folder set to:" + self.localdir)
        elif self.checkdirnotempty(self.instdir):
            self.chatbot.train(self.instdir)
            print("Training folder set to:" + self.instdir)

    def reply(self, phrase=""):
        response = self.chatbot.get_response(phrase)
        return response

    @staticmethod
    def checkdirnotempty(folder=""):
        check = False
        if os.path.isdir(folder):
            entities = os.listdir(folder)
            for entities in entities:
                if os.path.isfile(folder + entities):
                    check = True
                    break
        return check
