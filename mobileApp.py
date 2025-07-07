import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import re

# === CONFIG ===
input_folder = "ugcVids"
output_folder = "mobileApp_Output"
product_folder = "mobileApp_Products"
font_size = 52
font_color = "white"
bg_color = "transparent"  # Transparent background
font_name = "Calibri-Bold"

# === Ensure output folder exists ===
os.makedirs(output_folder, exist_ok=True)

# === Captions Array ===
captions = [
    "My face when I saw {title} for just €{price} {shipping}.",
    "€{price} and free shipping for {title}? You've got to be kidding me.",
    "Can't believe these {title} are only €{price} {shipping}.",
]

# === Get list of videos, sorted ===
video_files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
])

# === Process each video ===
for i, video_file in enumerate(video_files):
    # Use a simple caption for mobile app (no product placeholders)
    caption = captions[i % len(captions)]  # Cycle through captions
    
    input_path = os.path.join(input_folder, video_file)

    # Sanitize caption for filename (remove/replace invalid characters)
    def sanitize_filename(s):
        # Remove invalid characters for Windows filenames
        s = re.sub(r'[\\/:*?"<>|]', '', s)
        s = s.strip()
        return s

    # Get file extension
    _, ext = os.path.splitext(video_file)
    # Windows max filename length is 255, but need to leave room for extension
    MAX_FILENAME_LEN = 255 - len(ext)
    safe_caption = sanitize_filename(caption)
    truncated_caption = safe_caption[:MAX_FILENAME_LEN]
    output_filename = f"{truncated_caption}{ext}"
    output_path = os.path.join(output_folder, output_filename)

    print(f"▶️ Processing: {video_file}")
    print(f"   ➤ Caption: \"{caption}\"")

    try:
        clip = VideoFileClip(input_path)

        txt_clip = TextClip(
            caption,
            fontsize=font_size,
            color=font_color,
            font=font_name,
            stroke_color="black",
            stroke_width=2,
            bg_color=bg_color,
            size=(clip.w * 0.85, None),  # 85% width like ttShop.py
            method='caption',
            kerning=2
        ).set_duration(min(3, clip.duration))

        # Position: about 25% from the top (matching ttShop.py)
        txt_clip = txt_clip.set_position(("center", int(clip.h * 0.25)))

        # Cut the video to 3 seconds max
        final_clip = clip.subclip(0, min(3, clip.duration))
        final = CompositeVideoClip([final_clip, txt_clip])
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f"✅ Saved to: {output_path}\n")
    except Exception as e:
        print(f"❌ Error with {video_file}: {e}\n")
