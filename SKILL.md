---
name: TikTok Finance Video Generator
description: Generates a TikTok-style 9:16 video breakdown of monthly financial transactions with background images, text overlays, and background music.
---

# TikTok Finance Video Skill

This skill allows you to take a monthly list of financial transactions and automatically generate a polished TikTok video.

## Prerequisites
1. Analyze the user's provided transactions and sum them into logical high-level categories (e.g., Housing, Food, Utilities, College Tuition).
2. For each category, formulate an image generation prompt (e.g., "A modern brick college building on a sunny day" for "College Tuition").
3. Use your `generate_image` tool to generate an image for each category. Save these images in a temporary directory (e.g., `/tmp/finance_images/`).

## Generation Steps
1. Create a JSON file (e.g., `transactions.json`) in the same temporary directory mapping each generated image filename to its text label to overlay. Example format:
```json
{
  "housing.png": "Housing: $2,500",
  "college.png": "College Tuition: $1,200",
  "food.png": "Food & Dining: $800"
}
```
2. Run the `generate_video.py` script provided in this skill's `scripts/` directory to create the text overlays, apply transitions, and add the "Succession" opening music.
   ```bash
   python /Users/skyang/create/tiktok-finance-skill/scripts/generate_video.py \
     --image-dir /tmp/finance_images/ \
     --json /tmp/finance_images/transactions.json \
     --output /tmp/finance_tiktok_video.mp4 \
     --download-music
   ```
3. (Optional) Provide the final generated `/tmp/finance_tiktok_video.mp4` to the user and clean up the temporary directory.

## Required Setup
Ensure the required Python dependencies and system binaries are present before running:
- `pip install Pillow`
- `pip install yt-dlp` (if --download-music is used)
- Ensure `ffmpeg` is installed on the system (e.g., `brew install ffmpeg`).
