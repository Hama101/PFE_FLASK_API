'''
Pass it a filename and it will return a secure version of it. 
This filename can then safely be stored on a regular file 
system and passed to os.path.join(). 
The filename returned is an ASCII only string for maximum portability.
'''
from flask import *
import os
from werkzeug.utils import secure_filename
import label_image
from youtuber import search_youtube
from food52er import search_food52

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
    if request.method == 'POST':
        data = {
            'name': '',
            'youtube': [],
            'embeded': [],
            'blog_list': [],
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
        
        #set the data
        data['name'] = result
        data['youtube'] , data['embeded'] = search_youtube(result)
        data['blog_list'] = search_food52(result)

        return data
    return None


if __name__ == '__main__':
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    try : 
        app.run(host='192.168.1.13', port=8000)
    except :
        app.run()
