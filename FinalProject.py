# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 13:45:59 2014

@author: Klubien
"""

import nltk, random
from nltk.corpus import names
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

gutenberg_books = ['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'bible-kjv.txt', 'blake-poems.txt', 'bryant-stories.txt', 'burgess-busterbrown.txt', 'carroll-alice.txt', 'chesterton-ball.txt', 'chesterton-brown.txt', 'chesterton-thursday.txt', 'edgeworth-parents.txt', 'melville-moby_dick.txt', 'milton-paradise.txt', 'shakespeare-caesar.txt', 'shakespeare-hamlet.txt', 'shakespeare-macbeth.txt', 'whitman-leaves.txt']

def gender_features(word):
    features = {}
    features['last_letter'] = word[-1].lower()
    features['last_two_letters'] = word[-2:].lower()
    features['last_is_vowel'] = (word[-1].lower() in 'aeiouy')
    features['first_two_letters'] = word[:2].lower()
    return features

### Natural Language Processing with Python (O'Reilly 2009) ###
def define_gender(name_input):
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(labeled_names)

    featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
    train_set, test_set = featuresets[-500:], featuresets[:500]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
 
    return classifier.classify(gender_features(name_input))

def author_name(text):
    
    text = text[:100]
    tag = text.split()
    author = []

    current_tag = 0    
    for word in tag:        
        if word.lower() == ('by') or word.lower() == ('author') or word.lower() == ('author:'):
            author.append(tag[current_tag+1])
            current_tag+=1
            tag = tag[current_tag+1:]
            continue
        current_tag+=1
    
    current_tag = 0
    for word in tag:
        if tag[current_tag].istitle():
            author.append(tag[current_tag])
            current_tag+=1

    return author

def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def publication_year(text):
    tag = text.split()
    for word in tag:
        if is_number(word[0]):
            if is_number(word[1]):
                if is_number(word[2]):
                    if is_number(word[3]):
                        return word[0] + word[1] + word[2] + word[3]

## http://blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk/ ##                      
def language_propability(text):
    text = text[:500]
    lang_ratio = {}
    
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    
    for lang in stopwords.fileids():
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        intersection = words_set.intersection(stopwords_set)
        lang_ratio[lang] = len(intersection)
        
    prob_lang = max(lang_ratio, key = lang_ratio.get)
    
    return prob_lang
    
def extract_features(text):
    
    with open(text, 'rb') as f:
        book = f.read()
    
    raw_book = book.read().decode('utf8')
    current_book = text
    author = author_name(raw_book)
    author_gender = define_gender(author[0])
        

### Extract features from all books in Gutenberg collection
    
book_list = []
for book in gutenberg_books:
    current_book = nltk.corpus.gutenberg.raw(book)
    author = author_name(current_book)
    author_gender = define_gender(author[0])
    year = publication_year(current_book)
    lang = language_propability(current_book)
    
    book_data = {'Book': book, 'Author': author, 'Author gender': author_gender, 'Publication year': year, 'Book language': lang}
    book_list.append(book_data)

for book in book_list  :  
    print book
    print
