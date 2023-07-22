import streamlit as st
import random
import json 
import pickle 
import numpy as np 
from PIL import Image


import nltk 
from nltk.stem import WordNetLemmatizer


from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = pickle.load(open("models/words.pkl", "rb"))
classes = pickle.load(open("models/classes.pkl", "rb"))
model = load_model("models/terobik_model.h5")

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

# while True:
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)


with st.sidebar:
    st.markdown('<i class="far fa-smile"></i> Tombol dengan Ikon Font Awesome', unsafe_allow_html=True)

    st.write("""
        # TEROBIK
        UKM ORBIT - UIN Sjech M.Djamil Djambek Bukittinggi
    """)
    with st.expander("Tentang Kami"):
        st.write("""
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        """)
        st.image("https://static.streamlit.io/examples/dice.jpg")

    with st.echo():
        st.write("This code will be printed to the sidebar.")

with st.chat_message("assistant"):
        st.write("Halo Terobik disini!, saya adalah Kecerdasan Buatan yang dibuat & diprogram oleh UKM ORBIT")

if 'chat' not in st.session_state:
    st.session_state['chat'] = []


prompt = st.chat_input("Say something")

if prompt: 
    print("Pertanyaan : ", prompt)
    ints = predict_class(prompt)
    res = get_response(ints, intents)
    print("Jawaban : ", res)
    st.session_state['chat'].append({
        "pertanyaan" : prompt,
        "jawaban" : res
    })

    

for item in st.session_state['chat'] :
    with st.chat_message("user"):
        st.write(item["pertanyaan"])
    with st.chat_message("assistant"):
        st.write(item["jawaban"])


