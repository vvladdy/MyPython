# pip install SpeechRecognition
# pip install PyAudio (или найти версию данной библиотеки на сайте https://www.lfd.uci.edu/)

import speech_recognition as sr
import webbrowser
from os import path


def record_volume():

    r = sr.Recognizer()

    try:
        with sr.Microphone(device_index=1) as sourse:
            r.adjust_for_ambient_noise(source=sourse, duration=0.5) # прослушка шума
            # стороннего
            print('Listening...')
            audio = r.listen(source=sourse)
            query = r.recognize_google(audio_data=audio, language='ru-RU').lower()
            print(f'You told {query}')
        with open('speech_to_text.txt', 'w', encoding='utf-8') as file:
            file.write(query)


        return query
    except sr.UnknownValueError as error:
        print('Не понял, что вы сказали, повторите...', record_volume())

search_label = record_volume()

webbrowser.open("https://www.google.com/search?q=" + str(search_label))
