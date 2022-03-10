# Neural network car classifier


![Alt text](/screenshots/infographics.png?raw=true "Explanation")


This application is a Flask (https://flask-httpauth.readthedocs.io/en/latest/) app serving as a classifier for car images. It provides an interface to a Tensorflow (https://www.tensorflow.org) model that predicts the carmaker of the car on the submitted image.

The app is structured as both a template-based Flask application and an API which could be used completely independently. 

The __frontend__ directory contains a plain Javascript frontend which uses the Flask API but currently it is not yet implemented completely.

The __backend__ directory contains the Flask web app / API. The subdirectory __backend.app.classification_model__ contains a script for creating the Tensorflow model.


### Homepage
![Alt text](/screenshots/homepage.png?raw=true "Homepage")


### Example input image
![Alt text](/screenshots/input_image.png?raw=true "Prediction result")


### Prediction of 3 most probable classes based on the input image
![Alt text](/screenshots/prediction_result.png?raw=true "Prediction result")

### Information related to the most probable class
![Alt text](/screenshots/predicted_car_info.png?raw=true "Prediction result")
