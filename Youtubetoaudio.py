import os
import subprocess
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
import noisereduce as nr

def download_audio_from_youtube(video_url, output_path='audio'):
    """Downloads the entire audio from YouTube in WAV format and returns the path to the WAV file."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    output_file = os.path.join(output_path, '%(title)s.%(ext)s')  # yt-dlp format spec
    try:
        # Run yt-dlp to download audio in WAV format
        subprocess.run([
            'yt-dlp',
            '--no-cache-dir',
            '-x', '--audio-format', 'wav',  # Extract audio in WAV format
            '--audio-quality', '0',  # Best quality
            '-o', output_file,              # Specify output file name format
            video_url
        ], check=True)
        print("Audio download complete.")
        
        # Find the downloaded WAV file (yt-dlp uses video title as file name)
        for file in os.listdir(output_path):
            if file.endswith('.wav'):
                return os.path.join(output_path, file)
    except subprocess.CalledProcessError as e:
        print(f"Error during download: {e}")
        raise

def reduce_noise(input_audio_path, output_audio_path):
    """Reduces background noise in an audio file."""
    # Load the audio file
    rate, data = wavfile.read(input_audio_path)
    
    # If stereo, convert to mono
    if len(data.shape) == 2:
        data = data.mean(axis=1).astype(data.dtype)
    
    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=0.9)
    
    # Save the noise-reduced audio
    wavfile.write(output_audio_path, rate, reduced_noise)
    return output_audio_path

def extract_audio_sections(audio_file_path, sections, output_dir='output_audio'):
    """Extracts specific sections of the audio and saves them as separate WAV files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    audio = AudioSegment.from_file(audio_file_path)
    extracted_files = []
    
    for i, (start, end) in enumerate(sections):
        start_ms = start * 1000  # Convert seconds to milliseconds
        end_ms = end * 1000
        extracted_audio = audio[start_ms:end_ms]
        output_file = os.path.join(output_dir, f'section_{i+1}.wav')
        extracted_audio.export(output_file, format='wav')
        extracted_files.append(output_file)
        print(f"Section {i+1} saved as {output_file}")
    
    return extracted_files

# Example Usage
if __name__ == '__main__':
    video_url = input("Enter the YouTube video URL: ")
    sections = [(130,165)]  # Specify sections in seconds
    output_folder = '/home/coder-sf/Audioclips'  # Specify custom folder here

    # Step 1: Download entire audio from YouTube
    raw_audio_path = download_audio_from_youtube(video_url)
    print(f"Audio downloaded at: {raw_audio_path}")
    print(f"Downloaded audio file: {raw_audio_path}")  

    # Step 2: Reduce background noise on the entire audio
    noise_reduced_audio_path = raw_audio_path.replace('.wav', '_cleaned.wav')
    print("Reducing background noise...")
    cleaned_audio_path = reduce_noise(raw_audio_path, noise_reduced_audio_path)
    print(f"Noise-reduced audio saved at: {cleaned_audio_path}")
    
    # Step 3: Extract specified sections of the cleaned audio to the custom output folder
    extracted_files = extract_audio_sections(cleaned_audio_path, sections, output_dir=output_folder)
    print("Extracted audio files:", extracted_files)

