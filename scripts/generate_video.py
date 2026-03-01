import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def download_music(output_path):
    print("Downloading Succession theme music from SoundCloud...")
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--ffmpeg-location", "/opt/homebrew/bin/ffmpeg",
        "-o", str(output_path),
        "scsearch1:succession theme"
    ]
    subprocess.run(cmd, check=True)
    return output_path
    return output_path

def create_text_overlay(image_path, text, output_path, target_size=(1080, 1920)):
    # Open and resize/crop to 9:16 target size
    img = Image.open(image_path).convert('RGB')
    
    # Calculate crop to center
    img_ratio = img.width / img.height
    target_ratio = target_size[0] / target_size[1]
    
    if img_ratio > target_ratio:
        # Image is wider than target
        new_width = int(img.height * target_ratio)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    else:
        # Image is taller than target
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))
        
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # Create overlay
    txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt_layer)
    
    # Try to load a nice font, fallback to default
    try:
        # Try a common system font, Arial or San Francisco
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except IOError:
        font = ImageFont.load_default()
        
    # Draw text shadow/background for legibility
    bbox = d.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (target_size[0] - text_w) // 2
    y = (target_size[1] - text_h) // 2
    
    if text:
        # Draw semi-transparent background box behind text
        padding = 40
        d.rectangle(
            [x - padding, y - padding, x + text_w + padding, y + text_h + padding],
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        d.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # Combine
    out = Image.alpha_composite(img.convert('RGBA'), txt_layer)
    out.convert('RGB').save(output_path)

def create_video(image_files, music_file, output_music_video, durations=5):
    # Create a complex filter string for ffmpeg to concatenate and add transitions
    # For a simple version without crossfades, we just concatenate
    
    # Create an input text file for ffmpeg concat demuxer
    concat_file = "ffmpeg_concat.txt"
    with open(concat_file, 'w') as f:
        for i, img in enumerate(image_files):
            f.write(f"file '{img}'\n")
            if i == len(image_files) - 1:
                f.write(f"duration 5\n")
            else:
                f.write(f"duration {durations}\n")
        # Due to a quirk in concat demuxer, repeat last file
        f.write(f"file '{image_files[-1]}'\n")
            
    # Calculate video length
    video_length = (len(image_files) - 1) * durations + 5
    
    # ffmpeg command to mix video and audio, and loop/trim audio to fit
    cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-stream_loop", "-1",  # loop audio
        "-i", str(music_file),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",           # finish encoding when the shortest stream ends (the video concat)
        "-t", str(video_length), # ensure exact length
        str(output_music_video)
    ]
    
    print("Running FFmpeg to create video...")
    subprocess.run(cmd, check=True)
    os.remove(concat_file)
    print(f"Video saved to {output_music_video}")

def main():
    parser = argparse.ArgumentParser(description="Generate TikTok Finance Video")
    parser.add_argument("--image-dir", required=True, help="Directory containing background images")
    parser.add_argument("--json", required=True, help="JSON file mapping image filenames to text overlays")
    parser.add_argument("--output", required=True, help="Output MP4 file path")
    parser.add_argument("--download-music", action="store_true", help="Download Succession theme")
    
    args = parser.parse_args()
    
    image_dir = Path(args.image_dir)
    with open(args.json, 'r') as f:
        data = json.load(f)
        
    music_file = image_dir / "music.mp3"
    if args.download_music:
        download_music(music_file)
    else:
        # Assuming you have it or will provide it manually if not downloading
        if not music_file.exists():
            print(f"Warning: {music_file} not found. Ensure audio exists or use --download-music.")
            sys.exit(1)
            
    processed_images = []
    
    for img_filename, text in data.items():
        img_path = image_dir / img_filename
        if not img_path.exists():
            print(f"Skipping {img_filename}, not found in {image_dir}")
            continue
            
        out_path = image_dir / f"processed_{img_filename}"
        create_text_overlay(img_path, text, out_path)
        processed_images.append(out_path)
        
    if not processed_images:
        print("No images processed!")
        sys.exit(1)
        
    create_video(processed_images, music_file, args.output)
    
if __name__ == "__main__":
    main()
