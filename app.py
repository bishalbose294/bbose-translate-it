from flask import Flask, render_template,  url_for, request, send_file, redirect
import googletrans
from googletrans import Translator
import pyaudio
import wave
import speech_recognition as sr
import gtts
from playsound import playsound
import os
import librosa
import soundfile as sf


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods = ['POST'] )
def textEngToHin():
    
    print("Recieved Audio File")
    file = request.files['file']
    print('File from the POST request is: {}'.format(file))
    
    filename = "audio-preprocess.wav"
    if os.path.isfile(filename):
      os.remove(filename)
    with open(filename, "wb") as aud:
      aud_stream = file.read()
      aud.write(aud_stream)
    x,_ = librosa.load(filename, sr=16000)
    filename = "audio.wav"
    if os.path.isfile(filename):
      os.remove(filename)
    sf.write(filename, x, 16000)
    AUDIO_FILE = (filename) 
    r = sr.Recognizer() 
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)   
    try: 
      var = r.recognize_google(audio)
      #print("The audio file contains: " + var) 
    except sr.UnknownValueError: 
      print("Google Speech Recognition could not understand audio") 
    except sr.RequestError as e: 
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except Exception  as e:
      print(e)
    translator = Translator()
    result = translator.translate(var, src='en', dest='hi')
    #print(result.text)
    # make request to google to get synthesis
    tts = gtts.gTTS(result.text, lang='hi')
    translated_filename = 'translated.wav'
    if os.path.isfile(translated_filename):
      os.remove(translated_filename)
    # save the audio file
    tts.save(translated_filename)
    
    print('Sending data...')
    return send_file(translated_filename, as_attachment=False)


if __name__ == '__main__':
    app.run(debug=False)