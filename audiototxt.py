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
    
given_args = parser.parse_args()
audio_file = given_args.audiofile

# Audio files
AUDIO_SRC = audio_file
AUDIO_DST = f"{AUDIO_SRC}.wav"

# Converting audio to wav
logging.debug(f"{GREEN}Coverting audio to .wav file.{RESET}")
audio = AudioSegment.from_mp3(AUDIO_SRC)
audio.export(AUDIO_DST, format="wav")

# Selecionando  audio 
audio = AudioSegment.from_file(AUDIO_DST, 'wav')

# Tamanho
segment_size = 30000

# Segmenting  audio file
logging.debug(f"{GREEN}Segmenting audio file.{RESET}")

partes = make_chunks(audio, segment_size)
partes_audio = []


for i, parte in enumerate(partes):
    # Enumerando arquivo particionado
    parte_name = f"parte{i}.wav"
    # Guardando na lista
    partes_audio.append(parte_name)
    # Exportando arquivos
    parte.export(parte_name, format='wav')
    logging.debug(f"Audio segment created: {parte_name}")


def transcript_audio(name_audio):
    """This function trascript the audio file
    to string.

    Args:
        name_audio (str): name of audio file

    Returns:
        str : result of audio content in text string
    """
    # Select the audio file
    r = sr.Recognizer()
    with sr.AudioFile(name_audio) as source:
        audio = r.record(source) # Reading audio file

    try:
        logging.debug(f"Google Speech Recognition: Transcript {name_audio}")
        text = r.recognize_google(audio,language='pt-BR')
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
    with alive_bar(len(partes_audio), dual_line=True, title='Transcription') as bar:
        for parte in partes_audio:
            text = f"{text} {transcript_audio(parte)}"
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
