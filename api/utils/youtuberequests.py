
import requests

def query_yt(query, maxResults):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos = []
    search_params = {
        'key': "AIzaSyBhHpy8hkV8vu_fa5Pt025Kaz24BzWwc8M",
        'q': query,
        'part': 'snippet',
        'maxResults': maxResults,
        'type': 'video'
    }

    r = requests.get(search_url, params=search_params)

    results = r.json()['items']
    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    video_params = {
        'key': "AIzaSyBhHpy8hkV8vu_fa5Pt025Kaz24BzWwc8M",
        'id': ','.join(video_ids),
        'part': 'snippet,contentDetails,statistics',
        'maxResults': maxResults
    }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']
    for result in results:
        video_data = {
            'id': result['id'],
            'url': f'https://www.youtube.com/watch?v={result["id"]}',
            'thumbnail': result['snippet']['thumbnails']['high']['url'],
            'title': result['snippet']['title'],
            "viewCount": result["statistics"]["viewCount"],
            "likeCount": result["statistics"]["likeCount"],
            "dislikeCount": result["statistics"]["dislikeCount"],
        }
        videos.append(video_data)
    print(videos)
    return (videos)

def change_result_format_for_template(video_array):
    result = []
    index = 0
    temp_result = []
    for video in video_array:
        if index < 4:
            temp_result.append(video)
            index+=1
        else:
            result.append(temp_result)
            temp_result = []
            index = 0
    if len(temp_result) != 0:
        result.append(temp_result)
    return result
if __name__ == "__main__":
    print(query_yt("elif dj set",1))