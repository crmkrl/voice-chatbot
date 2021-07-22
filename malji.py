import io
import random
import string
import warnings
from nltk import text
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

from gtts import gTTS       #additional plugins
import os
import speech_recognition as speech 
import pyaudio
import time
from langdetect import detect, language
from langdetect import detect_langs
from deep_translator import GoogleTranslator
import nltk
from nltk.stem import WordNetLemmatizer
import responses

nltk.download('popular', quiet=True)
nltk.download('punkt')
nltk.download('wordnet') 

#Dataset
with open('txt/malji_dataset.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#Tokenisation
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#returning responses
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in responses.GREETING_INPUTS:
            return random.choice(responses.GREETING_RESPONSES)

def translate(text, from_lang, to_lang):
    translation = GoogleTranslator(source=from_lang, target=to_lang).translate(text)  # output -> Weiter so, du bist großartig
    return translation

def gTTS_cmd(txt, language):  #text to audio
    # myobj = gTTS(text=txt, lang=language, slow=False)
    # myobj.save("malji.mp3")
    # os.system("mpg321 malji.mp3")
    print(txt)

def speech_cmd():  #audio to text
    with speech.Microphone() as source:
        audio= recog.listen(source)
    try:
        user_response = format(recog.recognize_google(audio))
        return user_response
    except speech.UnknownValueError:
        gTTS_cmd(random.choice(responses.AUDIO_ERROR))
        pass

import string
import pprint
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def count_vec(sent_tokens):
    preprocessed_data = []
    for i in sent_tokens:
        preprocessed_data.append(i.split(' '))
    # frequency_list = []
    # for i in preprocessed_data:
    #     frequency_list.append(Counter(i))

    #bag of words
    count_vector = CountVectorizer(sent_tokens)
    count_vector.fit(sent_tokens)
    doc_array = count_vector.transform(sent_tokens).toarray()    

    col_names=count_vector.get_feature_names()
    frequency_matrix = pd.DataFrame(doc_array,index=sent_tokens,columns=col_names)
    print(frequency_matrix[preprocessed_data[-1]])

def response(user_response, lang):  #pulling out from dataset
    robo_response=''
    sent_tokens.append(user_response)       #per sentences stopping words
    count_vec(sent_tokens)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"My apologies, I am only a robot and under development."
        if lang!="en":
            robo_response=translate(robo_response, "english", lang)
        gTTS_cmd(robo_response, lang)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        if lang!="en":
            robo_response=translate(robo_response, "english", lang)
        gTTS_cmd(robo_response, lang)
        return robo_response

#initial greetings
with open('txt/initial.txt','r', encoding='utf8', errors ='ignore') as fin:
    malji_greetings = fin.read().lower()
    gTTS_cmd(malji_greetings, "en")

flag=True   
recog = speech.Recognizer()
while(flag==True):
    user_response = input()         #for readline  
    # user_response = speech_cmd()  #for voice command

    #idle...waiting for input
    if user_response is None:
        gTTS_cmd(random.choice(responses.QUIET_ERROR), "en")
        time.sleep(3)
    else:
        lang = detect(user_response)    
        if lang != "en":
            user_response = translate(user_response, lang, "en")
        user_response=user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                gTTS_cmd("You are welcome.", lang)
            else:
                if(greeting(user_response)!=None):
                    gTTS_cmd(greeting(user_response), "en")
                else:
                    response(user_response, lang)
                    sent_tokens.remove(user_response)
        else:
            flag=False  
            gTTS_cmd("Good bye!", lang)

