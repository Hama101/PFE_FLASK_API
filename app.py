'''
Pass it a filename and it will return a secure version of it. 
This filename can then safely be stored on a regular file 
system and passed to os.path.join(). 
The filename returned is an ASCII only string for maximum portability.
'''
from flask import *
import os
from werkzeug.utils import secure_filename
from googler import predict_image
from waitress import serve
from youtuber import search_youtube
from food52er import search_food52

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
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


@app.route('/<name>', methods=['GET'])
def get_vedios(name):
    print("name : ", name)
    data = {
        "vedios": [],
        "recpies": [],
    }
    if name:
        data['vedios'] = search_youtube(name)
        data['blog_list'] = search_food52(name)
    else:
        data = {
            "Error": "Error!"
        }
    return data


if __name__ == '__main__':
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    app.run(threaded=True, port=5000)
    # serve(app, host='0.0.0.0', port=5000)  # <---- ADD THIS
