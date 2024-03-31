import sys
import boto3
import os
import librosa
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import IPython.display as ipd
from requests import request
from PyPDF2 import PdfReader

def create_audio_display(y, sr, text=''):
    """
    Displays the audio player

    Args:
        y - the time series audio data
        sr - the sampling rate
        text - the text of the audiodisplay
    """
    plt.figure(figsize=(10,3))
    plt.plot(y, color='black')
    plt.xlim([0, y.shape[0]])
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()
    ipd.display(ipd.Audio(data=y, rate=sr))

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) != 2:
        print('Usage: "python main.py <filename>.pdf"')
    else:
        infile = sys.argv[1]
        bin_f = open('pdf_text.mp3' , 'wb')
        txt_f = open('pdf_text.txt', 'w')
        if infile.endswith('.pdf'):
            client = boto3.client('polly')
            reader = PdfReader(infile)
            for page in range(len(reader.pages)):
                text = reader.pages[page].extract_text()
                txt_f.write(text)
            txt_f.close()
            with open("pdf_text.txt") as f:
                text = f.read()
            response = client.synthesize_speech(
                OutputFormat="mp3",
                Text=text,
                VoiceId="Amy"
            )
            mp3_bytes = response['AudioStream'].read()
            bin_f.write(mp3_bytes)
            bin_f.close()
            # TODO: fix the program to work for larger pdf files.
            y, sr = librosa.load('pdf_text.mp3')
            create_audio_display(y, sr, text=sys.argv[1])
            client.close()

