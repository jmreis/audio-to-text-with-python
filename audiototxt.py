#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""CLI app for transcript an audio .wav to a .txt file."""
import os
import argparse
import logging
import timeit
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from alive_progress import alive_bar


# Cleaning terminal
os.system("clear")

# Setting terminal colors
RED = "\033[31;1m"
GREEN = "\033[32;1m"
CIANO = "\033[36;1m"
RESET = "\033[0;0m"

# Setting header ascii art
HEADER = f"""
       ▓╜▓▓▓▓▓▓                             ┌   █▌                        ┐┌
       ▀╛▓▓▓▓▓▓                            █▌   █▌                          ╙
   ▓▓▓▓▓▓▓▓▓▓╬╬░███     ╒█▀▀└▀█▄ ▐█░   ╫█ └▀█▀╙ ██▀▀▀██  ▄█▀╙▀█▄ ╔█▀╙╚▀█═
  ║▓▓▓▓▓▓▓▓▓▓▓╙▄███▌    ▐█    ╫█ ▐█░   ║█  ╫▌   █▌   ▐█ ▐█    ▐█ ╫█    █▌
  ╙▓▓▓▒████████████▌    ▐█    ▐█ ▐█═   ▐█  ╫▌   █▌   ▐█ ▐█    ▐█ ▐█    █▌
   ╙▓▓▒████▀▀▀▀▀▀▀▀     ▐█▀▄▄█▀░  ▀█▄▄╛▀█  └▀▄─ █▌   ▐█  ╙▀▄▄▄▀─ ▐█    █▒
       ██████▀█░        ▐█             ▄█
       ╙▀▀██▀▀▀         └▀          ╪▀▀▀
    {GREEN}---------------------------------------------------------------------------------
                            CONVERTING AUDIO TO TXT FILE
                                    by Jair Reis 
    ---------------------------------------------------------------------------------{RESET} 
"""
print(HEADER)

# Setting the logging configurations
logging.basicConfig(format='%(asctime)s - audiototxt.py - %(message)s', level=logging.DEBUG)

# Get start time
starttime = timeit.default_timer()
logging.debug(f'⏱ {GREEN}Start time: {starttime}{RESET}')

# Seting comand line
parser = argparse.ArgumentParser(description="Converting audio file to a trascript .txt file")
parser.add_argument("--audiofile", help="name of audio file with extension [Ex.: audio.mp3]",
 type=str, default="audio.mp3")
parser.add_argument("--lang-code", help="translation language code [Ex.: pr-BR ,...]",
 type=str, default="pt-BR", dest='lang_code')

given_args = parser.parse_args()
audio_file = given_args.audiofile

# Audio files
AUDIO_SRC: str = audio_file
REQUESTED_TRANSLATION_LANG_CODE: str = given_args.lang_code

# Converting audio to wav
logging.debug(f"{GREEN}Coverting audio to .wav file.{RESET}")
if not AUDIO_SRC.lower().endswith('.wav'):
    audio = AudioSegment.from_mp3(AUDIO_SRC)
    AUDIO_SRC = AUDIO_SRC + '.cvrt2.wav'
    audio.export(AUDIO_SRC, format="wav")

# Selecionando  audio 
audio = AudioSegment.from_file(AUDIO_SRC, 'wav')

# Tamanho
segment_size = 30000

# Segmenting  audio file
logging.debug(f"{GREEN}Segmenting audio file.{RESET}")

partes = make_chunks(audio, segment_size)


def transcript_audio(name_audio, lang_code: str='pt-BR'):
    """This function trascript the audio file
    to string.

    Args:
        name_audio (str): name of audio file
        lang_code  (str): code of translation language code (valid codes : https://cloud.google.com/speech-to-text/docs/languages)

    Returns:
        str : result of audio content in text string
    """
    # Select the audio file
    r = sr.Recognizer()
    with sr.AudioFile(name_audio) as source:
        audio = r.record(source) # Reading audio file

    try:
        logging.debug(f"Google Speech Recognition: Transcript {name_audio}")
        text = r.recognize_google(audio, language=lang_code)
    except sr.UnknownValueError:
        logging.debug(f'{CIANO}Google Speech Recognition NÃO ENTENDEU o audio.{RESET}')
        text = ''
    except sr.RequestError as e:
        logging.debug(f'{RED}Erro ao solicitar resultados do serviço Google Speech Recognition; {e}{RESET}')
        text = ''
    return text


if __name__ == "__main__":
    # Trascription of audios segments
    text = ''
    with alive_bar(len(partes), dual_line=True, title='Transcription') as bar:
        for i, parte in enumerate(partes):
            parte_name = f"parte{i+1}.wav"
            parte.export(parte_name, format='wav')
            text = f"{text} {transcript_audio(parte_name, REQUESTED_TRANSLATION_LANG_CODE)}"
            bar()
    logging.debug(f'{RED}Transcript of the audio file:{RESET}')
    print(text)

    # Save data in a .txt file
    with open("audio.txt", "w") as file:
        file.write(text)
    logging.debug(f"📝 {GREEN}Created audio.txt file{RESET}")
     
    # Cleaning segment audios
    logging.debug(f"🗑 {GREEN} Cleaning segment audios.{RESET}")
    os.system("rm -rf parte*")
    
    # Show the the time of script
    logging.debug(f'⏱ {GREEN}End time: {timeit.default_timer() - starttime}{RESET}')
