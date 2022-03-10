import os
from http import HTTPStatus

from flask import Blueprint, request, current_app
from flask import Response as FlaskResponse
from flask_pydantic_spec import Request, Response
from werkzeug.datastructures import FileStorage
import app.common.helpers as helpers
import app.common.constants as C
from app.api.logic.webapp_logic import CarDetailsObtainer
from app.common.models import ClassificationResult, CarDetails
from app.dependencies.apispec import apispec

restapi = Blueprint('restapi', __name__, url_prefix="/api")

@restapi.route('/classify',methods=[C.POST_METHOD])
# @cross_origin()
@apispec.validate(resp=Response(HTTP_200=ClassificationResult, HTTP_400=None), tags=['classify'])
def get_classification_result():
    try:
        file: FileStorage = request.files['file']
        saved_file_path, hash_with_filename = helpers.get_filepath(file, os.getenv(C.ENV_IMAGE_UPLOADS))
        file.save(saved_file_path)
        classificationresult: ClassificationResult = helpers.get_car_probabilities(saved_file_path, os.getenv(
            C.ENV_MODEL_PATH), os.getenv(C.ENV_CLASSMAPPING_PATH))
        response = classificationresult.dict()
        return response
    except:
        current_app.logger.exception(C.THERE_WAS_PROBLEM_PROCESSING)
        return FlaskResponse(status=HTTPStatus.BAD_REQUEST, response=C.THERE_WAS_PROBLEM_PROCESSING)


@restapi.route('/cardetails/<car>',methods=["GET"])
# @cross_origin()
@apispec.validate(resp=Response(HTTP_200=CarDetails, HTTP_400=None), tags=['car_details'])
def get_car_details(car: str):
    cd_obtainer = CarDetailsObtainer()
    car_details: CarDetails = cd_obtainer.obtain_car_details(car)