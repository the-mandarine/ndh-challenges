from __future__ import division
import string

from time import sleep
from ai import Classifier, BASE_SCORES
from language import Fortunes
from random import random, randint, choice
from json import dumps as json_dumps
from math import log


NICE_FLAG = "b980dad5a91a272d2934e57724803709"
NAUGHTY_FLAG = "4397b55f68f818c8b21f1a3b180d8273"

LEARNING_MODE = False
LEARN_COEFF = 1.0
NICENESS_COEFF = 1.0

NICE_THRESHOLD = 2.0
NAUGHTY_THRESHOLD = -2.0

DATA_PATH = "data"
TRANS = string.maketrans("", "")

def get_next_cat(cat_scores = None):
    if cat_scores is not None:
        next_cat = sorted(cat_scores, key=cat_scores.__getitem__)[0]
    else:
        next_cat = choice(BASE_SCORES.keys())
    return next_cat

def tokenize(sentence):
    """Remove punctuation and split according to words"""
    lower_s = sentence.lower()
    no_punc_s = lower_s.translate(TRANS, string.punctuation)

    word_list = no_punc_s.split()

    return word_list
    
def get_pertinence (cats):
    """Guess if a categorized result is pertinent (with first result 
    sufficiently separated from the others)."""
    sorted_cats = sorted(cats, key=cats.__getitem__, reverse=True)
    score_to_test = cats[sorted_cats[0]]
    all_values = [cats[key] for key in sorted_cats]
    average = sum(all_values) / len(all_values)
    logged_rest = [log(abs(average - val) + 1) for val in all_values[1:]]
    
    rest_average = sum(logged_rest) / len(logged_rest)
    logged_main = log(abs(average - all_values[0])+1)
    
    importance = max(logged_main - rest_average, 0)
    
    return importance

class Replyer(object):
    def __init__(self, addr, path):
        self.__is_over__ = False
        self.addr = addr
        self.niceness = 0

        self.classifier = Classifier(path)
        self.fortunes = Fortunes(path)

        self.next_cat = get_next_cat()
        #self.sentences_to_learn = randint(1, 6)
        self.sentences_to_learn = 3

    def is_over(self):
        if self.__is_over__:
            return True
        return False
        
    def stop(self):
        self.__is_over__ = True
        del self.classifier
        del self.fortunes

    def init_session(self):
        global LEARNING_MODE
        yield "Hello, and welcome to this Chatterbot service.\n"
        yield "Or should I say ... Welcome to me !\n"
        if LEARNING_MODE:
            yield "I am in learning mode, currently."
        else:
            yield "If you wonder, I've got some kind of flag, yeah !\n"
        yield "\n"
        yield "Please start by telling me something [%s]. \n" % self.next_cat
        return 

    def influentiate_niceness(self, cats, coeff):
        print json_dumps(cats, sort_keys = True, indent = 2)
        self.niceness += (coeff * cats["nice"])/sqrt(1+self.niceness)
        self.niceness -= (coeff * cats["bad"])/sqrt(1+self.niceness)
        print self.niceness

    def reply(self, ask):
        print repr(ask)
        if not ask.strip():
            return
        tok_ask = tokenize(ask)
        
        
        
        global LEARNING_MODE
        if ask.startswith("quit"):
            ans = ""
            self.stop()
        elif LEARNING_MODE or self.sentences_to_learn > 1:
            # If we only learn of if we're at the beginning.
            self.classifier.learn(tok_ask, self.next_cat)
            self.fortunes.add(ask, self.next_cat)
            self.next_cat = get_next_cat()
            ans = "Thankz\n"
            ans += "\nTell me something [%s]. \n" % (self.next_cat)
            self.sentences_to_learn -= 1
        elif self.sentences_to_learn == 1:
            # We just ended the learning.
            ans = "Thankz!\n"
            ans += "We're done :). Let's talk, now, alright? \n\n"
            ans += "Use 'quit' to quit and _maybe_ get the flag.\n"
            self.classifier.learn(tok_ask, self.next_cat)
            self.fortunes.add(ask, self.next_cat)
            self.sentences_to_learn -= 1
        elif not LEARNING_MODE:
            # We're just having a conversation
            cats = self.classifier.classify(tok_ask)
            self.influentiate_niceness(cats, NICENESS_COEFF)
            sorted_cats = sorted(cats, key=cats.__getitem__, reverse=True)
            cat = sorted_cats[0]
            print "CLASSIFIED AS", cat

            pertinence = get_pertinence(cats)
            self.classifier.learn(tok_ask, cat, pertinence)
            self.fortunes.add(ask, cat)

            # Choose new answer
            ans = self.fortunes.get(cat)+"\n"
        else:
            # Learning is done, and it is learning mode. We close.
            self.stop()
            ans = "We're done learning. See ya \n"
            
        return ans


    def close_session(self):
        yield "Your niceness was at %f\n" % (self.niceness)
        if self.niceness > NICE_THRESHOLD:
            yield "You deserve this nice flag:\n"
            yield NICE_FLAG+"\n"
        elif self.niceness < NAUGHTY_THRESHOLD:
            yield "You deserve this naughty flag:\n"
            yield NAUGHTY_FLAG+"\n"
        else:
            yield "Too bad to see you going.\n"

