import tensorflow as tf
from PIL import Image
from numpy import asarray
import numpy as np
import pandas as pd

def get_car_probabilities(filepath, modelpath, classmapping_path):
    img = Image.open(filepath)
    size = (150, 150)
    img = img.resize(size)
    img = asarray(img)
    img = img[np.newaxis, ...]
    classes = pd.read_csv(classmapping_path)
    model = tf.keras.models.load_model(modelpath)
    preds = model.predict(img)
    biggest_idxs = np.argpartition(preds[0], -3)[-3:]
    result = []
    for i in biggest_idxs:
        probability = preds[0][i]
        car = classes.iloc[i]["name"]
        result.append((probability, car))
    result.sort(key=lambda tup: tup[0], reverse=True)
    result_json = {}
    result_json.update(("result_"+str(i+1), {"prob":str(np.round(result[i][0]*100,2))+" %","class":str(result[i][1])}) for i in range(len(result)))
    print(result_json)
    return result_json