# coding=utf8
from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
from moviepy.editor import *
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def download_video(url):
    print("Downloading...")
    local_file = (
        YouTube(url)
        .streams.filter(progressive=True, file_extension="mp4")
        .first()
        .download()
    )
    print("Downloaded")
    return local_file

def validate_url(url):
    import validators

    if not validators.url(url):
        print("Hi there URL seems invalid ")

def cleanup():
    import pathlib
    import glob

    junks = glob.glob("*.mp4")
    for junk in junks:
        pathlib.Path(junk).unlink()

def generate_transcript(url,lang_api):
    id = url[url.index("=")+1:]        
    transcript = YouTubeTranscriptApi.get_transcript(id,languages=[lang_api])
    script = ""
    for text in transcript:
        t = text["text"]
        if t != '[Music]':
            script += t + " "		
    return script


def video_to_translate(url,initial_language,final_language):

    #Internal definitions
    if initial_language == "English":
        lang_in='en-US'
        lang_api='en'
    elif initial_language == "Italian":
        lang_in='it-IT'
        lang_api='it'
    elif initial_language == "Spanish":
        lang_in='es-MX'
        lang_api='es'
    elif initial_language == "Russian":
        lang_in='ru-RU'
        lang_api='rus'
    elif initial_language == "German":
        lang_in='de-DE'
        lang_api='de'
    elif initial_language == "Japanese":
        lang_in='ja-JP'
        lang_api='ja'
    if final_language == "English":
        lang='en'
    elif final_language == "Italian":
        lang='it'
    elif final_language == "Spanish":
        lang='es'
    elif final_language == "Russian":
        lang='ru'
    elif final_language == "German":
        lang='de'
    elif final_language == "Japanese":
        lang='ja'        

    file_obj=download_video(url)
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj)
    try:
        # Trying to get transcripts
        text = generate_transcript(url,lang_api)
    except Exception:
        print("NoTranscriptFound")
        # Trying to recognize audio
        # Insert Local Audio File Path
        videoclip.audio.write_audiofile("test.wav",codec='pcm_s16le')
    # initialize the recognizer
        r = sr.Recognizer()
        # open the file
        with sr.AudioFile("test.wav") as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data, language = lang_in)
        print(lang)

    # init the Google API translator
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    #translation.text
    trans=translation.text

    myobj = gTTS(text=trans, lang=lang, slow=False) 
    myobj.save("audio.wav") 
    # loading audio file
    audioclip = AudioFileClip("audio.wav")
    
    # adding audio to the video clip
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    new_video="video_translated_"+lang+".mp4"
    videoclip.write_videofile(new_video)
    #return 'audio.wav'
    return new_video

initial_language = gr.inputs.Dropdown(["English","Italian","Japanese","Russian","Spanish","German"])
final_language = gr.inputs.Dropdown([ "Russian","Italian","Spanish","German","English","Japanese"])
url =gr.inputs.Textbox(label = "Enter the YouTube URL below:")


gr.Interface(fn = video_to_translate,
            inputs = [url,initial_language,final_language],
            outputs = 'video', 
            verbose = True,
            title = 'Video Youtube Translator',
            description = 'A simple application that translates Youtube videos from English, Italian, Japanese, Russian, Spanish, and German  to  Italian, Spanish, Russian, English and Japanese.  Wait one minute to process.',
            article = 
                        '''<div>
                            <p style="text-align: center"> All you need to do is to upload the mp4 file and hit submit, then wait for compiling. After that click on Play/Pause for listing to the video. The video is saved in an mp4 format.
                            For more information visit <a href="https://ruslanmv.com/">ruslanmv.com</a>
                            </p>
                        </div>''',

           examples = [["https://www.youtube.com/watch?v=Cu3R5it4cQs&list", "English",'Italian']]             
           # examples=[['obama.mp4',"English",'Spanish'],
           #           ['obama.mp4',"English",'Italian'],
           #           ['obama.mp4',"English",'German'],
           #           ['obama.mp4',"English",'Japanese']
           #         ]         
            ).launch()