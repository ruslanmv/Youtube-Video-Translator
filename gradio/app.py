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

def validate_youtube(url):
    #This creates a youtube objet
    try:
        yt = YouTube(url)  
    except Exception:
        print("Hi there URL seems invalid")
        return True
    #This will return the length of the video in sec as an int
    video_length = yt.length
    if    video_length > 600:
        print("Your video is larger than 10 minutes")
        return True
    else:
        print("Your video is less than 10 minutes")
        return False

def validate_url(url):
    import validators
    if not validators.url(url):
        print("Hi there URL seems invalid ")
        return True
    else:
        return False   


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


def clean_transcript(transcript_list):
    script = ""
    for text in transcript_list:
        t = text["text"]
        if( (t != '[music]')  and  \
            (t != '[Music]')  and  \
            (t != '[музыка]') and  \
            (t != '[Музыка]') and  \
            (t != '[musik]')  and  \
            (t != '[Musik]')  and  \
            (t != '[musica]') and  \
            (t != '[Musica]') and  \
            (t != '[música]') and  \
            (t != '[Música]') and  \
            (t != '[音楽]')   and \
            (t != '[音乐]')     
          ) :
            script += t + " "
    return script
    
    
def get_transcript(url,desired_language):
    id_you= url[url.index("=")+1:]
    try: 
        # retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(id_you)

    except Exception:
        print('TranscriptsDisabled:')
        is_translated = False
        return " ", " ", is_translated 

    lista=[]
    transcript_translation_languages=[]
    # iterate over all available transcripts
    for transcript in transcript_list:
        lista.extend([
        transcript.language_code,
        transcript.is_generated,
        transcript.is_translatable,
        transcript_translation_languages.append(transcript.translation_languages),
                     ])
    print(lista)
    n_size=int(len(lista)/4)
    print("There are {} avialable scripts".format(n_size))
    import numpy as np
    matrix = np.array(lista)
    shape = (n_size,4)
    matrix=matrix.reshape(shape)
    matrix=matrix.tolist()
    is_manually=False
    is_automatic=False
    for lista in matrix: 
        #print(lista)
        language_code=lista[0]
        is_generated=lista[1]
        is_translatable=lista[2]
        if not is_generated and is_translatable : 
            print("Script found manually generated")
            is_manually=True
            language_code_man=language_code
        if  is_generated and is_translatable :
            print("Script found automatic generated")
            is_automatic=True
            language_code_au=language_code
            
    if  is_manually:
        # we try filter for manually created transcripts
        print('We extract manually created transcripts')
        transcript = transcript_list.find_manually_created_transcript([language_code]) 
  
    elif is_automatic:
        print('We  extract generated transcript')
        # or automatically generated ones, but not translated
        transcript = transcript_list.find_generated_transcript([language_code])
    else:
        print('We try find the transcript')
        # we directly filter for the language you are looking for, using the transcript list
        transcript = transcript_list.find_transcript([language_code])

    is_translated = False
    if is_translatable :
        for available_trad in  transcript_translation_languages[0]:
            if available_trad['language_code']==desired_language:
                print("It was found the translation for lang:",desired_language)
                print('We translate directly the transcript')
                transcript_translated =  transcript.translate(desired_language)
                transcript_translated=transcript_translated.fetch()
                translated=clean_transcript(transcript_translated)
                is_translated = True
    script_translated = ""            
    if is_translated :
        script_translated = translated

    transcript=transcript.fetch()
    script = clean_transcript(transcript)
        
    return script, script_translated, is_translated

# Set environment variables
home_dir = os.getcwd()
temp_dir=os.path.join(home_dir, "temp")
#Create temp directory
pathlib.Path(temp_dir).mkdir(parents=True, exist_ok=True)
os.environ['home_dir'] = home_dir
os.environ['temp_dir'] = temp_dir

def video_to_translate(url,initial_language,final_language):
    print('Checking the url')
    check =validate_youtube(url)
    if check is True: return "./demo/tryagain2.mp4"

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
    home_dir= os.getenv('home_dir')
    print('Initial directory:',home_dir)
    # Cleaning previous files
    cleanup()
    file_obj=download_video(url)
    print(file_obj)
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj)
    is_traduc=False
    # Trying to get transcripts

    text, trans, is_traduc = get_transcript(url,desired_language=lang)
    print("Transcript Found")

    if not is_traduc:
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
                        return "./demo/tryagain.mp4"
                    text=text+text_chunk+" "
                text=str(text)
                print(type(text))
                
            else:
                try:
                        text = r.recognize_google(audio_data, language = lang_in)
                except Exception:
                        print("This video cannot be recognized")
                        cleanup()
                        return "./demo/tryagain.mp4"
                
        #print(text)
        print("Destination language ",lang)

        # init the Google API translator
        translator = Translator()


        try:
            translation = translator.translate(text, dest=lang)
        except Exception:
            print("This text cannot be translated")
            cleanup()
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
            description = 'A simple application that translates Youtube small videos from English, Italian, Japanese, Russian, Spanish, and German  to  Italian, Spanish, Russian, English and Japanese.  Wait one minute to process.',
            article = 
                        '''<div>
                            <p style="text-align: center"> All you need to do is to paste the Youtube link and hit submit,, then wait for compiling. After that click on Play/Pause for listing to the video. The video is saved in an mp4 format.
                            The lenght video limit is 10 minutes. For more information visit <a href="https://ruslanmv.com/">ruslanmv.com</a>
                            </p>
                        </div>''',

           examples = [
                        ["https://www.youtube.com/watch?v=uLVRZE8OAI4", "English","Spanish"],
                        ["https://www.youtube.com/watch?v=fkGCLIQx1MI", "English","Russian"],
                        ["https://www.youtube.com/watch?v=6Q6hFtitthQ", "Italian","English"],
                        ["https://www.youtube.com/watch?v=s5XvjAC7ai8", "Russian","English"],
                        ["https://www.youtube.com/watch?v=qzzweIQoIOU", "Japanese","English"],
                        ["https://www.youtube.com/watch?v=nOGZvu6tJFE", "German","Spanish"]

                        ]           
            ).launch()