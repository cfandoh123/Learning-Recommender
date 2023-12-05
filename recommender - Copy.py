
import os
import googleapiclient.discovery
import requests
from bs4 import BeautifulSoup
import re
import base64
import numpy as np
from sklearn.decomposition import NMF
from sklearn.preprocessing import LabelEncoder



# # Set your YouTube Data API key
YOUTUBE_API_KEY = "AIzaSyD_xlg9gGZkIIRdNUyosA6JRv5MHDj6g_0"

def parse_duration(duration):
    # Use regular expressions to extract hours, minutes, and seconds from the duration string
    hours = re.findall(r'(\d+)H', duration)
    minutes = re.findall(r'(\d+)M', duration)
    seconds = re.findall(r'(\d+)S', duration)

    # Convert the extracted values to integers (if available) or default to 0
    hours = int(hours[0]) if hours else 0
    minutes = int(minutes[0]) if minutes else 0
    seconds = int(seconds[0]) if seconds else 0

    # Return the duration in hours, minutes, and seconds format
    return f"{hours}h {minutes}m {seconds}s"

def scrape_youtube_videos(topic):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get('YOUTUBE_API_KEY') or YOUTUBE_API_KEY

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    search_request = youtube.search().list(
        part="snippet",
        q=topic + " tutorial",
        type="video",
        maxResults=5  # Adjust the number of results as desired
    )
    search_response = search_request.execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]
    videos_request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    videos_response = videos_request.execute()

    videos = videos_response['items']
    sorted_videos = sorted(videos, key=lambda x: int(x['statistics']['likeCount']), reverse=True)

    print("----- YouTube Videos -----")
    for video in sorted_videos:
        title = video['snippet']['title']
        rating = video['statistics']['likeCount']
        views = video['statistics']['viewCount']
        duration = parse_duration(video['contentDetails']['duration'])
        author = video['snippet']['channelTitle']

        print("Title:", title)
        print("Rating:", rating)
        print("Views:", views)
        print("Duration:", duration)
        print("Author:", author)
        print("-------------------------------------------")
# Your Udemy API client ID and client secret
udemy_client_id = "lAm73qgv7AGOYHITYayvW9ysLulRZABZXlNhYyJY"
udemy_client_secret = "pv7GB5fBCE7BHANSOOZd2OJznZfaXMhulGXnkP5c74YhOoBmoCKtTHGo4ohy82eIaUHmeeyjQasc88wpQs6nygsJRrIkqp7RCPb8sIU0ZU6kN6ESjXkjnCR4DAbOIBaV"


def get_udemy_courses(topic):
    # Encode the credentials in Base64
    credentials = f"{udemy_client_id}:{udemy_client_secret}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # API endpoint
    url = f"https://www.udemy.com/api-2.0/courses/"

    # Make the authenticated API request
    headers = {"Authorization": f"Basic {base64_credentials}"}
    params = {
    "search": topic,
    "limit": 5  # Limit Udemy results to 5
}

    response = requests.get(url, headers=headers, params=params)

    # Process the API response
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        print("----- Udemy Courses -----")
        for course in data['results'][:5]:
            title = course['title']
            description = course['headline']
            course_picture = course['image_125_H']
            author = course['visible_instructors'][0]['title']
            price = course['price']

            if price is None or price == "":
                price = "Free"  # Replace None or empty string with "Free" for free courses

            print("Title:", title)
            print("Description:", description)
            print(course_picture)
            print("Author:", author)
            print("-------------------------------------------")
    else:
        print("API request failed:", response.status_code)







# Example usage
topic = input("Enter the topic you want to learn: ")

# Example usage
scrape_youtube_videos(topic)
get_udemy_courses(topic)













