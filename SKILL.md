---
name: TikTok Finance Video Generator
description: Generates a TikTok-style 9:16 video breakdown of monthly financial transactions with background images, text overlays, and background music.
---

# TikTok Finance Video Skill

This skill allows you to take a monthly list of financial transactions and automatically generate a polished TikTok video.

## Prerequisites
1. Analyze the user's provided transactions and sum them into 5-7 logical high-level categories sorted from most spent to least spent (e.g., Education, Taxes, Loans, Restaurants, Groceries, Shopping, Utilities).
2. For each category, formulate an image generation prompt (e.g., "A modern brick college building on a sunny day" for "Education") and use your `generate_image` tool to generate an image for each. Save these images in a temporary directory (e.g., `/tmp/finance_images/`). But first look in /tmp/finance_images for existing images. If they exist, use them. If not, generate them.
3. Generate an initial pie chart visualization using the included `scripts/generate_pie.py` script. First, create a temporary JSON file (e.g. `amounts.json`) that maps the category strings to numerical sums (e.g. `{"Housing": 2500.0, "Food": 800.0}`). Then execute the script to generate `intro.png` breaking down the visual split of transactions:
   ```bash
   python /Users/skyang/create/tiktok-finance-skill/scripts/generate_pie.py \
     --data /tmp/finance_images/amounts.json \
     --output /tmp/finance_images/intro.png \
     --title "Expenses for <month>/<year>\nStill grinding to\npay the bills"
   ```
4. Generate a final summary image using `generate_image` for the total screen (e.g. `total.png`).

## Generation Steps
1. Create a JSON file (e.g., `transactions.json`) in the same temporary directory mapping each generated image filename to its text label to overlay. Make sure to map the intro chart to an empty string `""` first, then list the category images IN SORTED descending order of spend, and finally the total screen using text emoticons like `:)` or `:(`.
Example format:
```json
{
  "intro.png": "",
  "education.png": "Education: $3,000",
  "housing.png": "Housing: $2,500",
  "food.png": "Food & Dining: $800",
  "total.png": "Total Spending: $6,300\nGoals for next month:\nspend less money :("
}
```
2. Run the `generate_video.py` script provided in this skill's `scripts/` directory to create the text overlays, apply transitions, and add the "Succession" opening music (from SoundCloud).
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
- `pip install Pillow matplotlib`
- `pip install yt-dlp` (if --download-music is used)
- Ensure `ffmpeg` is installed on the system (e.g., `brew install ffmpeg`).
