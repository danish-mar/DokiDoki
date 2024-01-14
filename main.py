import os
from pathlib import Path
from pytube import YouTube
from colorama import Fore, Style
import requests
from mutagen.id3 import ID3, APIC

# Helper function to print colored messages
def print_message(message, color):
    print(f"{color}{message}{Style.RESET_ALL}")

# Function to create a directory if it doesn't exist
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download video as MP3
def download_as_mp3(video, url):
    download_thumbnail(url)
    audio = video.streams.filter(only_audio=True).first()
    print_message("Downloading audio...", Fore.BLUE)
    mp3_filename = f"{video.title}.mp3"
    mp3_filepath = os.path.join("music", mp3_filename)
    audio.download(filename=mp3_filepath)  # Save as .mp3
    add_album_art(mp3_filepath, f"{video.title}.jpg")
    print_message("Audio downloaded successfully!", Fore.GREEN)

# Function to download video with selected quality
import string
def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)
    return sanitized_filename

def download_as_video(video):
    print_message("Available video formats:", Fore.YELLOW)
    streams = video.streams.filter(file_extension='mp4')
    for i, stream in enumerate(streams):
        print(f"{Fore.CYAN}{i+1}. {stream.resolution}{Style.RESET_ALL}")
    format_choice = int(input("Enter the number corresponding to the desired format: "))
    video_filename = sanitize_filename(video.title) + ".mp4"
    current_directory = os.getcwd()  # Get the current directory
    video_filepath = os.path.join("video", video_filename)
    streams[format_choice-1].download(filename=video_filepath)
    print_message("Video downloaded successfully!", Fore.GREEN)

# Function to download thumbnail
def download_thumbnail(url):
    try:
        video = YouTube(url)
        thumbnail_url = video.thumbnail_url
        thumbnail_filename = f"{video.title}.jpg"
        print_message("Downloading thumbnail...", Fore.BLUE)
        thumbnail = requests.get(thumbnail_url)
        with open(thumbnail_filename, "wb") as file:
            file.write(thumbnail.content)
        print_message("Thumbnail downloaded successfully!", Fore.GREEN)
    except Exception as e:
        print_message(f"Error downloading thumbnail: {str(e)}", Fore.RED)

# Function to add album art metadata
def add_album_art(mp3_file, image_file):
    if not os.path.isfile(mp3_file):
        print(f"{mp3_file} not found!")
        return
    
    if not os.path.isfile(image_file):
        print(f"{image_file} not found!")
        return
    
    try:
        # Create a new ID3 tag
        mp3 = ID3()
        
        # Add album art metadata to the MP3 file
        with open(image_file, 'rb') as image:
            mp3.add(APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',  # or 'image/png' if using a PNG image
                type=3,  # Album front cover
                desc='Cover',
                data=image.read()
            ))
        
        # Save the updated metadata to the MP3 file
        mp3.save(mp3_file)
        
        print(f"{mp3_file} metadata updated!")
        os.remove(image_file)
    except Exception as e:
        print(f"Error updating metadata: {str(e)}")

# Function to move a file to a specific location
def move_file(filename, destination):
    home = str(Path.home())
    destination_path = os.path.join(home, destination)
    create_directory_if_not_exists(destination_path)
    try:
        os.replace(filename, os.path.join(destination_path, filename))
    except Exception as e:
        print_message(f"Error moving file: {str(e)}", Fore.RED)

def main():
    # Create necessary folders if they don't exist
    create_directory_if_not_exists("video")
    create_directory_if_not_exists("music")

    url = input("Enter the YouTube video URL: ")
    try:
        video = YouTube(url)
        print_message(f"Video Title: {video.title}", Fore.CYAN)
        print_message(f"Channel: {video.author}", Fore.CYAN)
        print_message(f"Views: {video.views}", Fore.CYAN)
        print_message(f"Length: {video.length} seconds", Fore.CYAN)

        print_message("Select an option:", Fore.YELLOW)
        print("1. Download as MP3")
        print("2. Download as video")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            download_as_mp3(video, url)
        elif choice == 2:
            download_as_video(video)
    except Exception as e:
        print_message(f"An error occurred: {str(e)}", Fore.RED)

if __name__ == "__main__":
    main()
