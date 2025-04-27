import os
import json
import pandas as pd
from datetime import datetime

# Folder containing Instagram data
ig_folder = 'data/instagram'

# List to store all post data
all_ig_posts = []

# Loop through each file in the folder
for filename in os.listdir(ig_folder):
    if filename.endswith('.json') and filename.startswith('raw_'):
        filepath = os.path.join(ig_folder, filename)

        # Extract date and time from filename (e.g., 'raw_08-31-2024_06-00-16.json')
        date_str, time_str = filename.split('_')[1:3]  # ['08-31-2024', '06-00-16']
        
        # Reformat date to MM/DD/YYYY format
        post_date = datetime.strptime(date_str, '%m-%d-%Y').strftime('%m/%d/%Y')
        
        # Extract hour from time string (assumes 24-hour time)
        post_time = time_str.split('-')[0]  # '06' from '06-00-16'
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        posts = data.get('data', {}).get('posts', [])
        
        for post in posts:
            node = post.get('node', {})
            dimensions = node.get('dimensions', {})
            edge_media_to_caption = node.get('edge_media_to_caption', {}).get('edges', [])
            edge_media_to_comment = node.get('edge_media_to_comment', {})
            edge_media_preview_like = node.get('edge_media_preview_like', {})

            # Extract caption text if available
            caption_text = edge_media_to_caption[0]['node']['text'] if edge_media_to_caption else None

            # Extract tagged users and usernames
            tagged_edges = node.get('edge_media_to_tagged_user', {}).get('edges', [])
            tagged_users = [e['node']['user']['id'] for e in tagged_edges]
            tagged_usernames = [e['node']['user']['username'] for e in tagged_edges]
            verified_users = [e['node']['user']['is_verified'] for e in tagged_edges]

            # Extract post data
            post_info = {
                'post_id': node.get('id'),
                'post_type': node.get('__typename'),
                'media_width': dimensions.get('width'),
                'media_height': dimensions.get('height'),
                'is_video': node.get('is_video'),
                'tagged_users': tagged_users,
                'tagged_usernames': tagged_usernames,
                'verified_users': verified_users,
                'video_view_count': node.get('video_view_count'),
                'caption_text': caption_text,
                'comment_count': edge_media_to_comment.get('count'),
                'is_affiliate': node.get('is_affiliate'),
                'is_paid_partnership': node.get('is_paid_partnership'),
                'comments_disabled': node.get('comments_disabled'),
                'taken_at_timestamp': node.get('taken_at_timestamp'),
                'like_count': edge_media_preview_like.get('count'),
                'owner_id': node.get('owner', {}).get('id'),
                'owner_username': node.get('owner', {}).get('username'),
                'viewer_has_liked': node.get('viewer_has_liked'),
                'viewer_has_saved': node.get('viewer_has_saved'),
                'viewer_in_photo_of_you': node.get('viewer_in_photo_of_you'),
                'viewer_can_reshare': node.get('viewer_can_reshare'),
                'date': post_date,  # from filename
                'time': post_time,  # from filename
            }

            all_ig_posts.append(post_info)

# Create a DataFrame
instagram_df = pd.DataFrame(all_ig_posts)

# Convert 'date' column to datetime format for accurate sorting
instagram_df['date'] = pd.to_datetime(instagram_df['date'], format='%m/%d/%Y')

# Sort dataframe by 'date' and 'time' to ensure chronological order
instagram_df = instagram_df.sort_values(by=['date', 'time'], ascending=[True, True])

# Print first few rows
print(instagram_df.head())
