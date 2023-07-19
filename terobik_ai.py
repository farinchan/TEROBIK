import random
import json 
import pickle 
import numpy as np 
import pyttsx3
import speech_recognition as sr
import pyaudio

import nltk 
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

engine = pyttsx3.init()

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = pickle.load(open("model/words.pkl", "rb"))
classes = pickle.load(open("model/classes.pkl", "rb"))
model = load_model("model/terobik_model.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    try :
        tag = intents_list[0]["intent"]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                
                break 
        return result 
    except :
        return "Saya Belum Mengerti pertanyaan mu, walau saya adalah kecerdasan buatan tapi saya juga harus belajar lagi, heheh"

print("GO! Bot is running!")

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Halo perkenalkan nama ku adalah terobik!")
engine.runAndWait()

def SpeechRec():
    mendengar = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengar....")
        try:
            speech = mendengar.listen(source)
            print("Speech Diterima")
            speechText = mendengar.recognize_google(speech, language='id-ID')
            print("HUMAN : \t", speechText)
            return speechText
        except:
            print("Terjadi Kesalahan")
            return "Terjadi kesalahan"

while True:
    message = SpeechRec()
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("TEROBIK : \t", res)
    if res[0:22] == "Terobik Akan dimatikan":
        engine.say(res)
        engine.runAndWait()
        break 
    engine.say(res)
    engine.runAndWait()