import os
from typing import List

from flask import session

from app.common.models import CarDetails, VideoResult
import app.common.helpers as helpers
import app.common.constants as C

class CarDetailsObtainer():

    def obtain_car_details(self, car: str) -> CarDetails:
        query_string = car + " review"
        num_results = int(os.getenv(C.ENV_NUM_CAR_REVIEWS) or 10)
        car_reviews: List[VideoResult] = helpers.query_yt(query_string, num_results)
        wiki_summary = helpers.car_summary_from_wiki(car)
        try:
            car_file = session[C.SESSION_FILE_NAME]
        except KeyError:
            car_file = "No file was found"
        cardetails = CarDetails(
            wiki_summary = wiki_summary,
            carfile = car_file,
            car = car,
            review_videos = car_reviews
        )
        return cardetails