# pip install SpeechRecognition
# pip install PyAudio (или найти версию данной библиотеки на сайте https://www.lfd.uci.edu/)
# pip install pydub - для конвертации mp3 и т.д. в .wav
import time

import speech_recognition as sr
import webbrowser


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

        # можно записать во flac, aiff
        with open('audio.wav', 'wb') as audio_file:
            audio_file.write(audio.get_wav_data())

        return query
    except sr.UnknownValueError as error:
        print('Не понял, что вы сказали, повторите...', record_volume())

def from_audio_file(file):
    r = sr.Recognizer()

    with sr.AudioFile(file) as source:
        audio = r.record(source=source)
    try:
        querry = r.recognize_google(audio_data=audio, language='en')
        return f'File containe: {querry}'
    except sr.UnknownValueError:
        print('Ununderstandeble audio')

#search_label = record_volume()
#webbrowser.open("https://www.google.com/search?q=" + str(search_label))

# Текст из аудио-файла
print(from_audio_file('stop1.wav'))


#webbrowser.open("https://www.google.com/search?q=" + str(search_label))


