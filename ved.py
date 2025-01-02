import random
import requests
from moviepy import *
from PIL import Image
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pyGPT import aGPT
import textwrap  # Importing the textwrap module for text wrapping
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the IMAGE_API_KEY from the environment variable
IMAGE_API_KEY = os.getenv('IMAGE_API_KEY')

def fetch_images_from_picsum(query='nature', num_images=5):
    """
    Fetches images or videos from Pixabay based on the query.
    It can fetch either images or videos based on random media_type.

    Parameters:
    query (str): The search term for fetching images/videos.
    num_images (int): The number of images/videos to fetch.

    Returns:
    list: A list of image/video URLs.
    """
    images = []  # List to store the image/video URLs

    media_type = 0  # Choose random media type, 0 for images and 1 for videos
    per_page = num_images if num_images > 5 else 5  # Ensure minimum 5 results

    if media_type == 0:
        # Fetch images from Pixabay API
        url = 'https://pixabay.com/api'
        params = {
            'key': IMAGE_API_KEY,
            'q': query,
            'per_page': per_page,
            'image_type': 'vector',  # Specify image type (vector images)
            'min_width': 900,  # Minimum image width
            'min_height': 1600,  # Minimum image height
            "orientation": "vertical",  # Vertical orientation
            "order": "latest"  # Order by latest
        }
        # Make the GET request to the Pixabay API
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # If successful, process the image data
            data = response.json()
            for i, image in enumerate(random.sample(data['hits'], len(data['hits']))):
                if num_images > i:
                    # Add the image URL to the list
                    image_url = image['webformatURL']
                    image_name = f"pixabay_image_{i + 1}.jpg"
                    images.append(image_url)
                else:
                    break
        else:
            print("Failed to fetch images.")
    
    else:
        # Fetch videos from Pixabay API
        url = 'https://pixabay.com/api/videos/'
        params = {
            'key': IMAGE_API_KEY,
            'q': query,
            'per_page': per_page,
            'video_type': 'animation',  # Specify video type (animations)
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            # If successful, process the video data
            data = response.json()
            for i, video in enumerate(random.sample(data['hits'], len(data['hits']))):
                if num_images > i:
                    # Add the video URL to the list
                    video_url = video['videos']['large']['url']
                    video_name = f"pixabay_video_{i + 1}.mp4"
                    images.append(video_url)
                else:
                    break
        else:
            print("Failed to fetch videos.")
    
    return images

# Function to create a video with text and an image
def create_video_with_text_and_image(text, image_url, output_video_file="output_video.mp4", video_duration=20, font_path='Roboto-Regular.ttf'):
    """
    Creates a video using an image and overlaying text on it.

    Parameters:
    text (str): Text to display on the video.
    image_url (str): URL of the image to use as the background.
    output_video_file (str): The name of the output video file.
    video_duration (int): Duration of the video in seconds.
    font_path (str): The path to the font file to be used for the text.

    Returns:
    video: A moviepy video clip object.
    """
    # Fetch the image from the URL
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    
    # Resize the image to the desired resolution
    img = img.resize((900, 1600), Image.Resampling.LANCZOS) 
    
    # Create a semi-transparent black overlay to blend with the image
    black_overlay = Image.new("RGBA", img.size, (0, 0, 0, 128))  # RGBA: (R, G, B, A)
    
    # Blend the original image with the overlay
    blended_image = Image.blend(img.convert("RGBA"), black_overlay, alpha=0.5)
    blended_image_rgb = blended_image.convert("RGB")
    
    # Save the blended image temporarily
    image_file = "temp/temp_image.jpg"
    blended_image_rgb.save(image_file)
    
    # Load the image and create an image clip for the video
    image_clip = ImageClip(image_file, is_mask=False, transparent=False).with_duration(video_duration).resized(height=1600)
    
    # Wrap the text to fit within the desired width
    wrapped_text = wrap_text(text, width=37)
    
    # Create a text clip using the wrapped text
    text_clip = TextClip(text=wrapped_text,
                         font=font_path,
                         color='white', 
                         size=(900, 1600),
                         margin=(10,0),
                         stroke_color='black', 
                         stroke_width=8, 
                         method='label', 
                         font_size=50)
    
    # Set the duration and position of the text clip
    text_clip = text_clip.with_duration(video_duration).with_position('center')
    
    # Combine the image and text clips into a single video
    video = CompositeVideoClip([image_clip, text_clip], size=(900,1600))
    
    return video

# Function to add background music to the video
def add_audio_to_video(video, audio_file, output_video_with_audio_file="final_video.mp4"):
    """
    Adds background music to a video and outputs the final video.

    Parameters:
    video: The moviepy video clip object.
    audio_file (str): Path to the background music file.
    output_video_with_audio_file (str): The name of the output video file with audio.
    """
    # Load the audio file
    audio_clip = AudioFileClip(audio_file)
    
    # Set the audio to the video clip
    video = video.with_audio(audio_clip)
    
    # Write the final video with background music
    video.write_videofile(output_video_with_audio_file, codec="libx264", fps=24)

# Function to wrap text to fit within a specified width
def wrap_text(text, width=40):
    """Wraps the input text to fit within the specified width."""
    return "\n".join(textwrap.wrap(text, width))

# Convert Story Text to Speech (Audio)
def text_to_speech(text, output_filename="temp/story.mp3"):
    """
    Converts the input text into speech (MP3 format).

    Parameters:
    text (str): The text to convert into speech.
    output_filename (str): The name of the output audio file.
    """
    tts = gTTS(text=text, lang='hi', slow=True)  # Convert text to speech (using Hindi)
    tts.save(output_filename)  # Save the speech as an MP3 file

# Add Background Music to Audio
def add_background_music(audio_filename, music_filename, output_filename="temp/final_audio.mp3", combination=False):
    """
    Combines background music with voice audio.

    Parameters:
    audio_filename (str): Path to the voice audio file.
    music_filename (str): Path to the background music file.
    output_filename (str): The output filename for the combined audio.
    combination (bool): Whether to combine the music and voice or just use music.
    """
    # Load both the voice and background music
    voice = AudioSegment.from_mp3(audio_filename)
    music = AudioSegment.from_mp3(music_filename)
    
    # Decrease the volume of the background music
    music = music - 10  # Decrease volume by 10 dB
    
    # Match the duration of the music with the voice
    if len(music) > len(voice):
        music = music[:len(voice)+5000]  # Trim music if it's too long
    else:
        music = music * (len(voice) // len(music) + 1)  # Repeat music if it's too short
    
    # Combine the music and voice
    if combination:
        combined = voice.overlay(music)  # Mix music with voice
    else:
        combined = music  # Just use the music
    
    # Export the combined audio to an MP3 file
    combined.export(output_filename, format="mp3")

# Main script
if __name__ == "__main__":
    # Set the language and category zone for the content
    gpt = True
    language = random.choice([1,0,1,0,0])  # Randomly choose language (1 for Hindi, 0 for English)
    category_zone = 'Motivational'
    quote = random.choice(["motivational", "inspirational", "positivevibes kind of", "mindset thing", "growthmindset thing", "selfloveness", "innerstrength thing", "resilience", "nevergiveup", "believeinyourself", "keepgoing", "success", "journey", "lifequotes", "dailymotivation", "inspirationdaily", "quoteoftheday", "motivationmonday", "wisdom"])
    
    # Set language and font based on the random choice
    if language == 1:
        language = 'Hindi'
        font = "Kalam-Regular.ttf"
    else:
        language = "English"
        font = "Roboto-Regular.ttf"

    # Fetch text from GPT if enabled
    if gpt:
        engine = aGPT()
        query = f'''
    Can you write  2 lines about {quote} quote and do the below things -
    1. Provide only content.
    2. It should be in {language}.
    3. It should be maximum 50 words.
    4. It should be minimum 2 lines, use ; for new lines, and use simple humanized words.
    '''
        text = engine.ask(query)  # Get the generated text from GPT
        video_path = "final_video.mp4"
        title = engine.ask('Can you give a trending title for this in English, 5 words only, some words can be added as hashtags if trending')
        category_zone = engine.ask("Provide one word for the category in English")
        description = engine.ask("Provide description with a lot of trending hashtags")
        category = "22"
        tags = engine.ask("Provide minimum 5 tags, separated by commas")
    else:
        text = "हार मत मानो, मुश्किलें तो आती ही रहेंगी;  जीत तुम्हारी ही होगी, बस धैर्य रखो।"
    
    # Process and prepare the text for video creation
    text = text.replace('-', '-\n')  
    text = text.replace('–', '-\n')
    textList = text.split(";")
    
    # Fetch images to use in the video
    images = fetch_images_from_picsum(query=category_zone, num_images=len(textList))
    
    if images:
        # Choose background music
        bg_musics = [f'motivation-{i}.mp3' for i in range(10)]
        background_music_file = f'music/{random.choice(bg_musics)}'
        
        # Convert the text to speech
        text_to_speech(text)
        
        # Add background music to the speech audio
        add_background_music("temp/story.mp3", background_music_file, combination=False)

        # Randomly shuffle the images to ensure they are not in the same order
        random.shuffle(images)
        
        # Create video clips with text and images
        video_clips = []
        for i, img_url in enumerate(images):
            segment_text = f"{textList[i]}"
            video_clip = create_video_with_text_and_image(segment_text, img_url, video_duration=5, font_path='font/' + font)
            video_clips.append(video_clip)
        
        # Concatenate all the video segments into one final video
        final_video = concatenate_videoclips(video_clips)
        
        # Add the background music to the final video
        add_audio_to_video(final_video, 'temp/final_audio.mp3')
        
        print("Video with background music and random images has been generated successfully!")
        
        # Save metadata to a JSON file
        if gpt:
            with open('video-meta.json', 'w') as json_file:
                video_meta = {
                    "Video_content": text,
                    "title": title,
                    "description": description,
                    "category_zone": category_zone,
                    "tags": tags
                }
                json_file.write(json.dumps(video_meta, indent=4))

    else:
        print("Error: Could not fetch the images.")
