import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import re

# === CONFIG ===
captions_file = "captions.txt"
input_folder = "ugcVids"
output_folder = "mobileApp_Output"
product_folder = "mobileApp_Products"
font_size = 60
font_color = "white"
bg_color = "transparent"  # Transparent background
font_name = r"C:\\Windows\\Fonts\\Montserrat SemiBold.ttf"

# === Ensure output folder exists ===
os.makedirs(output_folder, exist_ok=True)

# === Read captions ===
with open(captions_file, "r", encoding="utf-8") as f:
    captions = [line.strip() for line in f if line.strip()]

# === Get list of videos, sorted ===
video_files = sorted([
    f for f in os.listdir(input_folder)
    if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
])

# === Check matching ===
min_count = min(len(captions), len(video_files))
if len(captions) != len(video_files):
    print(f"⚠️ Warning: {len(captions)} captions for {len(video_files)} videos. Only processing {min_count} matches.")

# === Process each matching pair ===
for i in range(min_count):
    caption = captions[i]
    video_file = video_files[i]

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
            stroke_width=2,  # Thicker outline
            bg_color=bg_color,
            size=(clip.w, None),
            method='caption',
            kerning=2  # Slightly increased letter spacing (if supported)
        ).set_duration(min(3, clip.duration))

        # Position: about 22% from the top
        txt_clip = txt_clip.set_position(("center", int(clip.h * 0.22)))

        # Cut the video to 3 seconds max
        final_clip = clip.subclip(0, min(3, clip.duration))
        final = CompositeVideoClip([final_clip, txt_clip])
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f"✅ Saved to: {output_path}\n")
    except Exception as e:
        print(f"❌ Error with {video_file}: {e}\n")
