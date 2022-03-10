from app.dependencies.apispec import apispec
from app.appfactory import application

apispec.register(application)
if __name__ == '__main__':
    application.run(debug=False)