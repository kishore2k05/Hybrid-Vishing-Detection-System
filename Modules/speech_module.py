import assemblyai as aai #type: ignore
import os
import subprocess
import sys
sys.path.append(os.path.dirname(__file__))
from gemini_module import convert_with_gemini

aai.settings.api_key = "c4fb0777665c48ad9f85e0e71ffe783d"
AUDIO_FOLDER = '../datasets/audio_files'
TRANSCRIPT_FOLDER = '../datasets/raw_transcripts'
TRANSLATED_FOLDER = '../datasets/translated_transcripts'
CLEANED_FOLDER = '../datasets/cleaned_transcripts'

def save_transcript(original_filename, text):
    if not os.path.exists(TRANSCRIPT_FOLDER):
        os.makedirs(TRANSCRIPT_FOLDER)
    
    base_name = os.path.splitext(original_filename)[0]
    save_path = os.path.join(TRANSCRIPT_FOLDER, base_name + ".txt")
    
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Saved raw transcript to: {save_path}")
    return save_path, base_name

def save_translated(base_name, text, language):
    if not os.path.exists(TRANSLATED_FOLDER):
        os.makedirs(TRANSLATED_FOLDER)
    
    lang_suffix = "_tanglish" if language == "Tanglish" else "_hinglish"
    save_path = os.path.join(TRANSLATED_FOLDER, base_name + lang_suffix + ".txt")
    
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Saved {language} translation to: {save_path}")
    return save_path, base_name + lang_suffix

def clean_with_rust(base_name, folder_type="raw"):
    print(f"Calling Rust text cleaner ({folder_type})...")
    
    try:
        result = subprocess.run(
            ['cargo', 'run', '--release', '--', base_name, folder_type],
            cwd='../text_cleaner',
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("Text cleaned successfully")
            return True
        else:
            print(f"Rust error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running Rust: {e}")
        return False

def transcribe_audio(audio_file_path):
    if not os.path.exists(audio_file_path):
        print(f"Error: File '{audio_file_path}' not found")
        return None
    
    try:
        print(f"\nProcessing Audio: {os.path.basename(audio_file_path)}...")
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            print(f"AssemblyAI Error: {transcript.error}")
            return None
        
        text = transcript.text
        print(f"Transcribed: {text[:100]}...")
        
        save_path, base_name = save_transcript(os.path.basename(audio_file_path), text)
        
        clean_with_rust(base_name, "raw")
        
        print("\nTranslating to Tanglish...")
        tanglish = convert_with_gemini(text, "Tanglish")
        if tanglish:
            _, tanglish_name = save_translated(base_name, tanglish, "Tanglish")
            clean_with_rust(tanglish_name, "translated")
        
        print("\nTranslating to Hinglish...")
        hinglish = convert_with_gemini(text, "Hinglish")
        if hinglish:
            _, hinglish_name = save_translated(base_name, hinglish, "Hinglish")
            clean_with_rust(hinglish_name, "translated")
        
        return text
        
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

def clean_all_translated():
    if not os.path.exists(TRANSLATED_FOLDER):
        print(f"Error: Folder '{TRANSLATED_FOLDER}' not found")
        return
    
    transcript_files = [f for f in os.listdir(TRANSLATED_FOLDER) if f.endswith('.txt')]
    
    if not transcript_files:
        print("No translated transcript files found")
        return
    
    print(f"\nFound {len(transcript_files)} translated transcripts to clean")
    print("="*60)
    
    for i, transcript_file in enumerate(transcript_files, 1):
        base_name = os.path.splitext(transcript_file)[0]
        print(f"\n[{i}/{len(transcript_files)}] Cleaning: {base_name}")
        clean_with_rust(base_name, "translated")
        print("-"*60)
    
    print("\n" + "="*60)
    print("All translated transcripts cleaned!")
    print("="*60)

def process_all_audio_files():
    if not os.path.exists(AUDIO_FOLDER):
        print(f"Error: Audio folder '{AUDIO_FOLDER}' not found")
        return
    
    audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.wav')]
    
    if not audio_files:
        print("No .wav files found in the audio folder")
        return
    
    print(f"Found {len(audio_files)} audio files to process\n")
    print("="*60)
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file}")
        audio_path = os.path.join(AUDIO_FOLDER, audio_file)
        transcribe_audio(audio_path)
        print("-"*60)
    
    print("\n" + "="*60)
    print("All audio files processed!")
    print("="*60)

if __name__ == "__main__":
    print("Starting batch processing...")
    process_all_audio_files()