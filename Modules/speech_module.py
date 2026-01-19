import assemblyai as aai
import os

aai.settings.api_key = "c4fb0777665c48ad9f85e0e71ffe783d"

FILE_PATH = '../datasets/audio_files/scam_01.wav'

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"

def transcribe_audio():
    if not os.path.exists(FILE_PATH):
        print(f"{RED}Error: File '{FILE_PATH}' not found!{RESET}")
        return None

    try:
        print(f"Processing Audio: {os.path.basename(FILE_PATH)}...")
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(FILE_PATH)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"{RED}AssemblyAI Error: {transcript.error}{RESET}")
            return None

        text = transcript.text
        print(f"{GREEN}Transcribed:{RESET} \"{text}\"")
        return text

    except Exception as e:
        print(f"{RED}Unexpected Error: {e}{RESET}")
        return None

if __name__ == "__main__":
    transcribe_audio()