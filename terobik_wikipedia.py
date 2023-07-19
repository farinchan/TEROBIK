import wikipedia as wiki
import speech_recognition as sr
from ttsmms import TTS, download
import wikipedia as wiki
import pygame
import pyttsx3

pygame.init()
engine = pyttsx3.init()

tts=TTS("data/ind") #update lang code

def SpeechRec():
    mendengar = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengar....")
        try:
            speech = mendengar.listen(source)
            print("Speech Diterima")
            speechText = mendengar.recognize_google(speech, language='id-ID')
            print(speechText)
        except:
            print("Terjadi Kesalahan")
            pass

def TextToSpeech():
    tts.synthesis("Halo Perkenalkan nama saya terobik. ada yang bisa saya bantu?", wav_path="sound/example.wav")
    my_sound = pygame.mixer.Sound('./sound/example.wav')
    my_sound.play()

def GG():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Halo perkenalkan nama ku adalah terobik!")
    engine.runAndWait()


def tanya():
    bertanya = input("Apa pertanyaan anda :")
    wiki.set_lang("id")
    menjawab = wiki.summary(bertanya)
    # tts.synthesis(menjawab, wav_path="jawaban.wav")
    # my_sound = pygame.mixer.Sound('./jawaban.wav')
    # my_sound.play()
    voices = engine.getProperty('voices')

    engine.setProperty('voice', voices[1].id)
    engine.say(menjawab)
    engine.runAndWait()

TextToSpeech()
# GG()
tanya()




# input = input()
# wiki.set_lang("id")
# search = wiki.summary(input)
# print(search)