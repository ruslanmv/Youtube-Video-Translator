# coding=utf8
# Youtube Video Translator
# Developed by Ruslan Magana Vsevolodovna
# https://ruslanmv.com/

# importing all necessary libraries
import pathlib
import sys, os
from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
from moviepy.editor import *
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from utils import *

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
    types = ('*.mp4', '*.wav') # the tuple of file types
    #Finding mp4 and wave files
    junks = []
    for files in types:
        junks.extend(glob.glob(files))
    try:    
        # Deleting those files
        for junk in junks:
            print("Deleting",junk)
            # Setting the path for the file to delete
            file = pathlib.Path(junk)
            # Calling the unlink method on the path
            file.unlink()               
    except Exception:
        print("I cannot delete the file because it is being used by another process")         

def getSize(filename):
    st = os.stat(filename)
    return st.st_size


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

    # Initial directory
    home_dir = os.getcwd()
    print('Initial directory:',home_dir)
    cleanup()
    # Temporal directory
    temp_dir=os.path.join(home_dir, "temp")
    print('Temporal directory:',temp_dir)
    #Create temp directory
    pathlib.Path(temp_dir).mkdir(parents=True, exist_ok=True)
    # Go to temp directory
    os.chdir(temp_dir)
    print('Changing temporal directory',os.getcwd())
    # Cleaning previous files
    cleanup()
    file_obj=download_video(url)
    print(file_obj)
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj)
    try:
        # Trying to get transcripts
        text = generate_transcript(url,lang_api)
        print("Transcript Found")
    except Exception:
        print("No Transcript Found")
        # Trying to recognize audio
        # Insert Local Audio File Path
        videoclip.audio.write_audiofile("audio.wav",codec='pcm_s16le')
    # initialize the recognizer
        r = sr.Recognizer()
        # open the file
        with sr.AudioFile("audio.wav") as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            print("Recognize from ",lang_in)
            #There is a limit of 10 MB on all single requests sent to the API using local file
            size_wav=getSize("audio.wav")
            if  size_wav > 50000000:
                print("The wav is too large")
                audio_chunks=split_audio_wav("audio.wav")
                text=""
                for chunk in audio_chunks:
                    print("Converting audio to text",chunk)
                    try:
                        text_chunk= r.recognize_google(audio_data, language = lang_in)
                    except Exception:
                        print("This video cannot be recognized")
                        cleanup()
                        # Return back to main directory
                        os.chdir(home_dir)
                        return "./demo/tryagain.mp4"
                    text=text+text_chunk+" "
                text=str(text)
                print(type(text))
                
            else:
                text = r.recognize_google(audio_data, language = lang_in)
        #print(text)
    print("Destination language ",lang)

    # init the Google API translator
    translator = Translator()


    try:
        translation = translator.translate(text, dest=lang)
    except Exception:
        print("This text cannot be translated")
        cleanup()
        # Return back to main directory
        os.chdir(home_dir)
        return "./demo/tryagain.mp4"
    
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
  
    # Return back to main directory
    os.chdir(home_dir)
    print('Final directory',os.getcwd())

    videoclip.write_videofile(new_video)

    videoclip.close()
    del file_obj

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
                            <p style="text-align: center"> All you need to do is to paste the Youtube link  and hit submit, then wait for compiling. After that click on Play/Pause for listing to the video. The video is saved in an mp4 format.
                            For more information visit <a href="https://ruslanmv.com/">ruslanmv.com</a>
                            </p>
                        </div>''',

           examples = [
                        ["https://www.youtube.com/watch?v=Cu3R5it4cQs&list", "English","Italian"],
                        ["https://www.youtube.com/watch?v=fkGCLIQx1MI", "English","Spanish"],
                        ["https://www.youtube.com/watch?v=fkGCLIQx1MI", "English","Russian"],
                        ["https://www.youtube.com/watch?v=_5YeX8eCLgA&ab_channel=TheTelegraph", "Russian","English"],
                        ["https://www.youtube.com/watch?v=qzzweIQoIOU", "Japanese","English"],
                        ["https://www.youtube.com/watch?v=eo17uDr2_XA", "German","Spanish"]
                        ]           
            ).launch()