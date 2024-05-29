from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

def split_text(text, max_length):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    chunks.append(" ".join(current_chunk))
    return chunks

def text_to_speech(text, filename, lang='tr'):
    tts = gTTS(text, lang=lang)
    tts.save(filename)

def text_to_image(text, image_filename, width=1280, height=720, font_path='DejaVuSans.ttf'):
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((width - text_width) // 2, (height - text_height) // 2)
    d.text(position, text, fill=(0, 0, 0), font=font)
    
    img.save(image_filename)

def create_video_from_text(text, output_filename):
    chunks = split_text(text, max_length=50)
    clips = []
    for i, chunk in enumerate(chunks):
        text_to_image(chunk, f"frame_{i}.png")
        text_to_speech(chunk, f"audio_{i}.mp3", lang='tr')
        
        audio_clip = AudioFileClip(f"audio_{i}.mp3")
        image_clip = ImageClip(f"frame_{i}.png").set_duration(audio_clip.duration).set_audio(audio_clip)
        clips.append(image_clip)
    
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_filename, fps=24)

text = "hisse senedi direnç seviyesinden destek seviyesine kadar açılacak yeni pozisyonlar risk taşır. yeni açılacak pozisyonlarda destek seviyeleri dikkate alınmalıdır."
create_video_from_text(text, "output_video.mp4")