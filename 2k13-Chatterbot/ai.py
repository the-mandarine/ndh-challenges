
import os
import sys
import pdb
from glob import iglob
from json import dumps as json_dumps, loads as json_loads
from itertools import chain
from math import log

WORDS_PATH = os.path.join("data", "words", "*.json")
OCCS_DIR = "occs"
OCCS_SUFFIX = "_occs.json"
WORDS_DIR = "words"
WORDS_SUFFIX = ".json"

BASE_SCORES = {
    "bad": 0.0,
    "nice": 0.0,
    "gene": 0.0,
}


def calculate_words_scores(path):
    occs = load_occs(path)
    all_words = set(chain.from_iterable(occs[cat].keys() for cat in occs))
    total_words = len(all_words)
    for word in all_words:
        # Calculate a score for each word according to tf-idf
        scores = {}
        total_occurrences = sum((occs[cat].get(word, [0, 0])[0]) for cat in occs)
        total_sessions = sum((occs[cat].get(word, [0, 0])[1]) for cat in occs)

        #####
        total_importance = 1 + log(total_occurrences * total_sessions + 1)
        #####
        for cat in occs:
            word_vals = occs[cat].get(word, [0, 0])
            occurrences = word_vals[0]
            sessions = word_vals[1]
            
            #####
            try:
                local_importance = log(1 + occurrences * sessions * sessions)
                cat_score = local_importance / total_importance
            except:
                pdb.set_trace()
            
            #####
            
            scores[cat] = cat_score
            # Store is in words/word.json
        score_string = json_dumps(scores, indent=2, sort_keys = True)
        word_path = os.path.join(path, 
                                 WORDS_DIR, 
                                 "%s%s" % (word, WORDS_SUFFIX)
                                )
            
        with open(word_path, 'w') as word_file:
            word_file.write(score_string)

def load_word(path, word):
    """Load specific word scores in its json fils"""
    word_path = os.path.join(path,
                             WORDS_DIR, 
                             "%s%s" % (word, WORDS_SUFFIX)
                            )
    if not os.path.isfile(word_path):
        return {}
    with open(word_path, 'r') as word_file:
        score_string = word_file.read()
    scores = json_loads(score_string)
    return scores


def get_cat_from_path(path):
    filename = os.path.basename(path)
    cat = filename[:-len(OCCS_SUFFIX)]
    return cat

def save_occs(path, new_occs):
    """Load the global occs, merge with it, save it"""
    #TODO Lock
    # Load
    occs = load_occs(path)
    # Merge
    for cat in new_occs:
        if not cat in occs:
            occs[cat] = {}
        try:
            for word in new_occs[cat]:
                if word in occs[cat]:
                    occs[cat][word][0] += new_occs[cat][word]
                    occs[cat][word][1] += 1
                else:
                    occs[cat][word] = [new_occs[cat][word], 1]
        except:
            pdb.set_trace()
        cat_occs_string = json_dumps(occs[cat], indent=2)
        cat_occs_path = os.path.join(path, OCCS_DIR, "%s%s" % (cat, OCCS_SUFFIX))
        # Store
        with open(cat_occs_path, 'w') as cat_occs_file:
            cat_occs_file.write(cat_occs_string)
    
    #TODO Unlock
    

def load_occs(path):
    """Load occurences from a path"""
    occs_pattern = os.path.join(path, OCCS_DIR, "*%s" % OCCS_SUFFIX)
    occs_paths = iglob(occs_pattern)
    all_occs = {}
    for occs_path in occs_paths:
        occs_cat = get_cat_from_path(occs_path)
        with open(occs_path, 'r') as occs_file:
            occs_string = occs_file.read()
        occs = json_loads(occs_string)
        all_occs[occs_cat] = occs

    return all_occs
    
class Classifier(object):

    def __init__(self, path):
        self.path = path
        self.personnal_occs = {}

        #self.scores = load_scores(path)

    def __del__(self):
        # Store occs
        save_occs(self.path, self.personnal_occs)


    def learn(self, tokens, category, pertinence = 1.0):
        """Just store tokens in the category"""
        for word in tokens:
            if category not in self.personnal_occs:
                self.personnal_occs[category] = {}

            if word in self.personnal_occs[category]:
                self.personnal_occs[category][word] += pertinence
            else:
                self.personnal_occs[category][word] = pertinence


    def classify(self, sentence, learn = 1.0):
        cats = BASE_SCORES.copy()
        sentence_length = len(sentence)
        for word in sentence:
            word_scores = load_word(self.path, word)
            
            for cat in word_scores:
                if cat in cats:
                    cats[cat] += word_scores[cat] / sentence_length
                else:
                    cats[cat] = word_scores[cat] / sentence_length
        
        return cats


def test_main():
    path = "data"
    calculate_word_scores(path)

if __name__ == '__main__':
    test_main()

