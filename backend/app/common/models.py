from typing import Dict, List

from pydantic import BaseModel

from app.common.enums import ClassificationPosition

import numpy as np

class VideoResult(BaseModel):
    Id: str
    url: str
    thumbnail_url: str
    title: str
    viewcount: int
    likecount: int

class CarModelPrediction(BaseModel):
    car: str
    probability: float

class ClassificationResult(BaseModel):
    results: Dict[ClassificationPosition,CarModelPrediction]

    def for_template(self) -> Dict:
        return {
            "result_"+str(i+1) : {
                "prob":str(np.round(self.results[ClassificationPosition(i)].probability*100,2))+" %",
                "class":str(self.results[ClassificationPosition(i)].car) }
            for i in range(len(self.results.keys()))}

class CarDetails(BaseModel):
    wiki_summary: str
    review_videos: List[VideoResult]
    carfile: str
    car: str

    def review_videos_to_template(self):
        return [
            {
                'id': x.Id,
                'url': x.url,
                'thumbnail': x.thumbnail_url,
                'title': x.title,
                "viewCount": x.viewcount,
                "likeCount": x.likecount
            } for x in self.review_videos
        ]