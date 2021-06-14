import os

def set_app_config(app):

    #app.config["PROJECT_PATH"] = os.getenv("PROJECT_PATH")
    #app.config["PROJECT_PATH"] = "/Users/janpresperin/Desktop/VIA/CarClassifierFlask/web"

    #app.config["IMAGE_UPLOADS"] = os.path.join(app.config["PROJECT_PATH"], "uploads")
    #app.config["MODEL_PATH"] = os.path.join(app.config["PROJECT_PATH"], "model/cars196model.h5")
    #app.config["CLASSMAPPING_PATH"] = os.path.join(app.config["PROJECT_PATH"], "model/class_mappings.csv")
    app.config["PROJECT_PATH"] = "/Users/janpresperin/Desktop/VIA/CarClassifierFlask/web"
    app.config["IMAGE_UPLOADS"] =  "./uploads"
    app.config["MODEL_PATH"] =  "./model/cars196model.h5"
    app.config["CLASSMAPPING_PATH"] =  "./model/class_mappings.csv"
    app.secret_key = "fdfudshfbdsfdsg5fd36g1323dfg02df2g"
    app.config["NUM_CAR_REVIEWS"] = 15
