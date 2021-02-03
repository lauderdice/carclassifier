1. Run classifier.py file in classifier folder. This fill generate a model file (I assume some basic knowledge of Tensorflow)
2. Change app.config["MODEL_PATH"] in web/utils/config to accomodate where your model is located. Also make sure to change other configs.
3. Build with:
`docker-compose up --build`