import os
from mutagen.id3 import ID3, APIC

mp3_file = input("Enter MP3 filename: ")
image_file = input("Enter image filename: ")

if not os.path.isfile(mp3_file):
    print(f"{mp3_file} not found!")
    exit()

if not os.path.isfile(image_file):
    print(f"{image_file} not found!")
    exit()

# Load the MP3 file's metadata
mp3 = ID3(mp3_file)

# Add album art metadata to the MP3 file
with open(image_file, 'rb') as image:
    mp3.add(APIC(
        encoding=3, # UTF-8
        mime='image/jpeg', # or 'image/png' if using a PNG image
        type=3, # Album front cover
        desc='Cover',
        data=image.read()
    ))

# Save the updated metadata to the MP3 file
mp3.save()
print(f"{mp3_file} metadata updated!")

