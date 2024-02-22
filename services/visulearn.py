# Random ass functions that belong in no specific place
from PIL import Image
import pytesseract
from gtts import gTTS
import secrets
import string
from pydub import AudioSegment
from moviepy.editor import *
import cv2
from gensim.summarization import summarize
from services.logger import get_logger

logger = get_logger()

def is_image(file):
    try:
        image = Image.open(file.file)
        image.verify()
        return True
    except:
        return False
    
def ocr(file):
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    return text

def summarise_text(text: str, ratio=0.2):
    summary = summarize(text, ratio=ratio)
    return summary

#TODO
# rn, only for english
def text_to_speech(text: str):
    tts_en = gTTS(text, lang='en')
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
    tts_en.save(f'{random_name}.mp3')
    return f'{random_name}.mp3'

def get_length_of_audio(filepath: str):
    audio = AudioSegment.from_file(filepath)
    duration_in_seconds = len(audio) / 1000  # Convert milliseconds to seconds
    return duration_in_seconds

def generate_images(text: str, num_images: int):
    #TODO
    pass

def get_title_from_text(text: str):
    #TODO
    pass

def final_video_production(image_paths: list[str], audio_path: str):
    duration_per_image = get_length_of_audio(audio_path) / len(image_paths)
    random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
    output_filename = random_name + ".mp4"

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30

    audio = AudioFileClip(audio_path)
    try:
        images_clip = ImageSequenceClip(image_paths, fps=fps, durations=[duration_per_image] * len(image_paths))
    except Exception as e:
        logger.error("Error creating image sequence clip: " + str(e))
        return None
    
    final_clip = images_clip.set_audio(audio)
    
    try:
        final_clip.write_videofile(output_filename, codec=codec)
    except Exception as e:
        logger.error("Error writing video file: " + str(e))
    return None