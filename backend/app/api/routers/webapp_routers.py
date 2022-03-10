import os
from typing import Dict

from werkzeug.datastructures import FileStorage

import app.common.helpers as helpers
from flask import Blueprint, render_template, request, session, send_from_directory
import app.common.constants as C
from app.api.logic.webapp_logic import CarDetailsObtainer
from app.common.models import ClassificationResult, CarDetails

webapp = Blueprint('app', __name__, url_prefix="/app")


@webapp.route('/', methods=[C.GET_METHOD])
# @cross_origin()
def main_page():
    return render_template('index.html')


@webapp.route('/classification_result',methods=[C.GET_METHOD, C.POST_METHOD])
# @cross_origin()
def get_classification_result():
    if request.method == C.POST_METHOD:
        file: FileStorage = request.files['file']
        saved_file_path, hash_with_filename = helpers.get_filepath(file, os.getenv(C.ENV_IMAGE_UPLOADS))
        file.save(saved_file_path)
        classificationresult: ClassificationResult = helpers.get_car_probabilities(saved_file_path, os.getenv(C.ENV_MODEL_PATH), os.getenv(C.ENV_CLASSMAPPING_PATH))
        classif_result_json: Dict = classificationresult.for_template()
        session[C.SESSION_CLASSIF_RESULT]: Dict = classificationresult.for_template()
        session[C.SESSION_FILE_NAME] = hash_with_filename
    elif request.method == C.GET_METHOD:
        try:
            classif_result_json: Dict = session[C.SESSION_CLASSIF_RESULT]
        except KeyError:
            return render_template('index.html')
    else:
        return render_template('index.html')
    return render_template("prediction.html", predictions = classif_result_json)



@webapp.route('/uploads/<filename>', methods=[C.GET_METHOD])
def uploaded_file(filename: str):
    return send_from_directory(os.path.join(os.getcwd(),os.environ.get(C.ENV_IMAGE_UPLOADS)),filename)


@webapp.route('/cardetails/<car>',methods=[C.GET_METHOD])
# @cross_origin()
def get_car_details(car: str):
    cd_obtainer = CarDetailsObtainer()
    car_details: CarDetails = cd_obtainer.obtain_car_details(car)
    return render_template('cardetails.html',
                           wiki=car_details.wiki_summary,
                           reviews=car_details.review_videos,
                           carfilename = car_details.carfile, car = car_details.car)