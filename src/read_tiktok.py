import json
import pandas as pd
import os
import re
from datetime import datetime

# Folder containing TikTok data
tiktok_folder = 'data/tiktok'

# Initialize an empty list to collect records
all_records = []

# Loop through all files in the folder
for filename in os.listdir(tiktok_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(tiktok_folder, filename)
        
        # Extract the datetime info from filename
        match = re.search(r'(\d{2})-(\d{2})-(\d{4})-(\d{2})', filename)
        if match:
            month, day, year, hour = match.groups()
            file_datetime = datetime(int(year), int(month), int(day), int(hour))
        else:
            continue  # Skip files that do not match the expected filename pattern
        
        # Load the JSON file
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Skip files with no "data" field or empty data
        if 'data' not in data or not data['data']:
            continue
        
        # Process each post in the "data" field
        for post in data['data']:
            # Extract relevant features
            record = {
                'file_datetime': file_datetime,  # from filename
                'create_time': post.get('create_time'),
                'author': post.get('added_sound_music_info', {}).get('author'),
                'follower_count': post.get('follower_count'),
                'following_count': post.get('following_count'),
                'favoriting_count': post.get('favoriting_count'),
                'total_favorited': post.get('total_favorited')
            }
            all_records.append(record)

# Create DataFrame
tiktok_df = pd.DataFrame(all_records)

# Print the head of the DataFrame
print(tiktok_df.head())
