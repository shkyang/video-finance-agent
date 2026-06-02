import shutil
import json
import os
from PIL import Image, ImageDraw

# create images dir
os.makedirs('/tmp/finance_images', exist_ok=True)

# copy images
artifact_dir = '/Users/skyang/.gemini/antigravity/brain/a1a8e78b-01b8-4d3a-ab1c-4d268b5ba858'
img_mappings = [
    ('education_png_1778473685207.png', 'education.png'),
    ('taxes_png_1778473760955.png', 'taxes.png'),
    ('travel_png_1778473895094.png', 'travel.png'),
    ('personal_png_1778473908209.png', 'personal.png'),
    ('loans_png_1778473953552.png', 'loans.png'),
    ('housing_png_1778473966749.png', 'housing.png'),
    ('food_png_1778473979313.png', 'food.png')
]

for src_name, dst_name in img_mappings:
    src_path = os.path.join(artifact_dir, src_name)
    dst_path = os.path.join('/tmp/finance_images', dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)

# create total.png
img = Image.new('RGB', (1080, 1920), color = (0, 0, 0))
d = ImageDraw.Draw(img)
d.text((540, 960), ":(", fill=(255, 255, 255))
img.save('/tmp/finance_images/total.png')

# create amounts.json
amounts = {
  "Education": 9704.83,
  "Taxes": 4460.43,
  "Travel & Transportation": 4280.69,
  "Personal & Family": 3293.89,
  "Loans": 2719.60,
  "Housing & Utilities": 1953.11,
  "Food & Dining": 1912.60
}
with open('/tmp/finance_images/amounts.json', 'w') as f:
    json.dump(amounts, f, indent=4)

# create transactions.json
transactions = {
  "intro.png": "",
  "education.png": "Education: $9,704",
  "taxes.png": "Taxes: $4,460",
  "travel.png": "Travel & Transportation: $4,280",
  "personal.png": "Personal & Family: $3,293",
  "loans.png": "Loans: $2,719",
  "housing.png": "Housing & Utilities: $1,953",
  "food.png": "Food & Dining: $1,912",
  "total.png": "Total Spending: $28,325\nGoals for next month:\nspend less money :("
}
with open('/tmp/finance_images/transactions.json', 'w') as f:
    json.dump(transactions, f, indent=4)

print("Setup complete")
