import os
from mutagen.id3 import ID3, APIC

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

add_album_art(mp3_file="120.mp3",image_file="1.jpg")