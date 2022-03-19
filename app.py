'''
Pass it a filename and it will return a secure version of it. 
This filename can then safely be stored on a regular file 
system and passed to os.path.join(). 
The filename returned is an ASCII only string for maximum portability.
'''

'''
this app is using selenium to predict the image than to scrape some data from websites it may take some time proccessing

'''

# from predict_ts import predict_image


# creating app with cross




from BD import Recipe, get_list_by_topic
from food52er import search_food52
from youtuber import search_youtube
from waitress import serve
from googler import predict_image
from werkzeug.utils import secure_filename
import os
from flask import *
from flask_cors import CORS
def load_image(image):
    print("Loading image...", image)
    return predict_image(image)


"""
Configure the app and views
"""


def create_app(register_stuffs=True):

    app = Flask(__name__)
    CORS(app)  # This makes the CORS feature cover all routes in the app

    if register_stuffs:
        register_views(app)
    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


# this view will be using selenuim to predict the image
@app.route('/api/v1/predict', methods=['GET', 'POST'])
def upload_v1():
    if request.method == 'POST':
        data = {
            "predections": []
        }
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        result = "Label"
        # # Make prediction
        print("image url : ", file_path)
        try:
            names, percentages, images = predict_image(file_path)
            for name, percentage, image in zip(names, percentages, images):
                data["predections"].append({
                    "id": f"{name}",
                    "name": name,
                    "percentage": percentage,
                    "image": str(image)
                })
        except Exception as e:
            print(e)
            # # Process your result for humans
            data["Error"] = "Error Whle Predicting the image"
        os.remove(file_path)
        # set the data here
        return data
    return None


# # this view will be using tensorflow to predict the image
# @app.route('/api/v2/predict', methods=['GET', 'POST'])
# def upload_v2():
#     if request.method == 'POST':
#         data = {
#             "predections": []
#         }
#         # Get the file from post request
#         f = request.files['file']
#         file_path = secure_filename(f.filename)
#         f.save(file_path)
#         result = "Label"
#         # # Make prediction
#         print("image url : ", file_path)
#         try:
#             names, percentages, images = load_image(file_path)
#             for name, percentage, image in zip(names, percentages, images):
#                 data["predections"].append({
#                     "id": f"{name}",
#                     "name": str(name),
#                     "percentage": str(percentage),
#                     "image": str(image)
#                 })
#         except Exception as e:
#             print(e)
#             # # Process your result for humans
#             data["Error"] = "Error Whle Predicting the image"
#         os.remove(file_path)
#         # set the data here
#         return data
#     return None


@app.route('/<name>', methods=['GET'])
def get_list_of_recipes(name):
    try:
        return {
            "data": get_list_by_topic(name)
        }
    except Exception as e:
        print(e)
        return {
            "Error": "Error while fetching data"
        }


@app.route('/recipe-details', methods=['POST'])
def recipe_details():
    try:
        data = request.get_json()
        url = data['url']
        recipe = Recipe(url)
        return {
            "data": recipe.get_data()
        }
    except Exception as e:
        print(e)
        return {
            "Error": "Error while fetching data"
        }


if __name__ == '__main__':

    app.run(threaded=True, port=5000)
    # serve(app, host='0.0.0.0', port=5000)  # <---- ADD THIS
