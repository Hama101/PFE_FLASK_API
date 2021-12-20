from flask import *
import os
from werkzeug.utils import secure_filename
import label_image
from youtuber import search_youtube

def load_image(image):
    print("Loading image...",image)
    text = label_image.main(image)
    return text


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    print("1")
    if request.method == 'POST':
        data = {
            'name': '',
            'youtube': '',
            'embeded': ''
        }
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        # Make prediction
        result = load_image(file_path)
        result = result.title()

        print(result)
        os.remove(file_path)
        
        data['name'] = result
        data['youtube'] , data['embeded'] = search_youtube(result)
        return data
    return None


if __name__ == '__main__':
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    try : 
        app.run(host='192.168.1.152', port=8000)
    except :
        app.run()
