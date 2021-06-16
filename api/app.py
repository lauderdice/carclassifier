import json
import os
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory
from werkzeug.utils import secure_filename
from model.model import get_car_probabilities
from utils.config import set_app_config
from utils.wikirequests import car_summary_from_wiki
from utils.youtuberequests import query_yt
import uuid
from flask_cors import CORS, cross_origin


from flask_swagger_ui import get_swaggerui_blueprint
app = Flask(__name__)
set_app_config(app)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CarClassifier"
    }
)
cors = CORS(app)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def main_page():
    return render_template('index.html')

@app.route('/classify_old',methods=["GET", "POST"])
@cross_origin()
def classify_old():
    if request.method == 'POST':
        file = request.files['file']
        hash_with_filename = str(uuid.uuid4().hex)+"_"+file.filename
        filename = secure_filename(hash_with_filename)
        filepath = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        file.save(filepath)
        classificationresult = get_car_probabilities(filepath, app.config["MODEL_PATH"], app.config["CLASSMAPPING_PATH"])
        session["classification_result"] = classificationresult
        session["filename"] = hash_with_filename
    else:
        try:
            classificationresult = session["classification_result"]
        except:
            return {}
    print("CL_RESULT",classificationresult)
    return classificationresult


@app.route('/classify',methods=["GET", "POST"])
@cross_origin()
def classify():
    if request.method == 'POST':
        file = request.files['carfile']
        hash_with_filename = str(uuid.uuid4().hex)+"_"+file.filename
        filename = secure_filename(hash_with_filename)
        filepath = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        file.save(filepath)
        classificationresult = get_car_probabilities(filepath, app.config["MODEL_PATH"], app.config["CLASSMAPPING_PATH"])
        session["classification_result"] = classificationresult
        session["filename"] = hash_with_filename
    else:
        try:
            classificationresult = session["classification_result"]
        except:
            return {}
    response = app.response_class(
        response=json.dumps(classificationresult),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response


@app.route('/cardetails/<car>',methods=["GET"])
@cross_origin()
def get_car_details(car):
    wiki_summary = ""
    if request.method == 'GET':
        query_string = car + " review"
        num_results = app.config["NUM_CAR_REVIEWS"]
        car_reviews = query_yt(query_string, num_results)
        wiki_summary = car_summary_from_wiki(car)
        session["wiki_summary"] = wiki_summary
        session["reviews"] = car_reviews
    try:
        car_file = session["filename"]
    except:
        car_file = "No file was found"
    print("WIKI",wiki_summary)
    print("REVW",car_reviews)
    print("CARFILE",car_file)
    print("CAR",car)
    data = {
        "wiki": wiki_summary,
        "reviews":car_reviews,
        "car": car
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGE_UPLOADS'],filename)



#app.run(host="0.0.0.0", debug=True,port=5000)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)