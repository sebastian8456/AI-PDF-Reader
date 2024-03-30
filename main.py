import sys
import boto3
import os
from dotenv import load_dotenv
from requests import request
from PyPDF2 import PdfReader

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) != 2:
        print('Usage: "python main.py <filename>.pdf"')
    else:
        infile = sys.argv[1]
        f = open('pdf_text.mp3' , 'w')
        if infile.endswith('.pdf'):
            client = boto3.client('polly')
            reader = PdfReader(infile)
            pages = len(reader.pages)
            for page in range(pages):
                text = reader.pages[page].extract_text()
                response = client.synthesize_speech(
                    OutputFormat="mp3",
                    Text=text,
                    VoiceId="Celine"
                )
                print(response["AudioStream"]())
                f.write(response)
            # TODO: Read the mp3 bytes aloud
                
            client.close()
        f.close('pdf_text.mp3')

