import os
import json
import pandas as pd
from datetime import datetime

# Folder containing TikTok data
tiktok_folder = 'data/tiktok'

# List to store all post data
all_tiktok_posts = []

# Loop through each file in the folder
for filename in os.listdir(tiktok_folder):
    if filename.endswith('.json') and filename.startswith('raw_'):
        filepath = os.path.join(tiktok_folder, filename)
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        posts = data.get('data', [])

        # Skip empty files (when posts is an empty list)
        if not posts:
            continue

        # Extract datetime from filename
        _, date_str, time_str = filename.replace('.json', '').split('_')
        file_datetime = datetime.strptime(f'{date_str}-{time_str}', '%m-%d-%Y-%H-%M-%S')

        for post in posts:
            author_info = post.get('author', {})
            author_stats = author_info.get('stats', {})

            post_info = {
                'file_datetime': file_datetime,
                'create_time': post.get('create_time', None),
                'author': post.get('added_sound_music_info', {}).get('author', None),
                'follower_count': author_stats.get('followerCount', None),
                'following_count': author_stats.get('followingCount', None),
                'favoriting_count': post.get('favoriting_count', None),  
                'total_favorited': author_stats.get('heart', None),
            }
            all_tiktok_posts.append(post_info)

# Create a DataFrame
tiktok_df = pd.DataFrame(all_tiktok_posts)

# Sort the dataframe by 'file_datetime'
tiktok_df = tiktok_df.sort_values(by='file_datetime')

# Print first few rows
print(tiktok_df.head(50))
