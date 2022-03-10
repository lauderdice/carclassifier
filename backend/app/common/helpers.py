import os
import uuid
from typing import List, Tuple
import app.common.constants as C
import requests
import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import pandas as pd
import wikipedia
from pandas import DataFrame
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.common.enums import ClassificationPosition
from app.common.models import ClassificationResult, CarModelPrediction, VideoResult


def get_car_probabilities(filepath: str, modelpath: str, classmapping_path: str) -> ClassificationResult:
    img = Image.open(filepath)
    size = (150, 150)
    img = img.resize(size)
    img = asarray(img)
    img = img[np.newaxis, ...]
    classes: DataFrame = pd.read_csv(classmapping_path)
    model = tf.keras.models.load_model(modelpath)
    preds = model.predict(img)
    biggest_idxs = np.argpartition(preds[0], -3)[-3:]
    result: List[Tuple[float, str]] = []
    for i in biggest_idxs:
        probability = preds[0][i]
        car = classes.iloc[i]["name"]
        result.append((probability, car))
    result.sort(key=lambda tup: tup[0], reverse=True)
    classif_result: ClassificationResult = ClassificationResult(results = {})
    for position, car_on_position in enumerate(result):
        classif_result.results[ClassificationPosition(position)] = \
            CarModelPrediction(
                car = str(result[position][1]),
                probability = float(result[position][0])
            )
    return classif_result

def car_summary_from_wiki(car_model_brand: str) -> str:
    try:
        car = car_model_brand.split(" ")[0]
        page = wikipedia.search(car)[0]
        text = wikipedia.page(page).summary
    except:
        text = "Unfortunately, CarClassifier was not able to find any information about this model on Wikipedia. Sorry."
    return text


def query_yt(query: str, maxResults: int = 10) -> List[VideoResult]:
    search_url = C.YOUTUBE_URL_SEARCH
    video_url = C.VIDEO_URL
    videos: List[VideoResult] = []
    search_params = {
        'key': os.getenv(C.ENV_YT_APIKEY),
        'q': query,
        'part': 'snippet',
        'maxResults': maxResults,
        'type': 'video'
    }

    r = requests.get(search_url, params=search_params)
    try:
        results = r.json()['items']
    except KeyError:
        results = []
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
    try:
        results = r.json()['items']
    except KeyError:
        results = []
    for result in results:

        video_data = VideoResult(
            Id = result['id'],
            url = f'https://www.youtube.com/watch?v={result["id"]}',
            thumbnail_url =  result['snippet']['thumbnails']['high']['url'],
            title = result['snippet']['title'],
            viewcount = int(result["statistics"].get("viewCount") or 0),
            likecount = int(result["statistics"].get("likeCount") or 0),
        )
        videos.append(video_data)
    return videos

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

def get_filehash(filename: str) -> str:
    return str(uuid.uuid4().hex)+"_"+filename


def get_filepath(file: FileStorage, image_uploads_dir: str) -> Tuple[str, str]:
    hash_with_filename = get_filehash(file.filename)
    filename = secure_filename(hash_with_filename)
    filepath = os.path.join(image_uploads_dir, filename)
    return filepath, hash_with_filename