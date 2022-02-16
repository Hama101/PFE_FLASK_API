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

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data = {
            'name': [],
            'percentage': [],
        }
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)
        result = "Label"
        # # Make prediction
        print("image url : ",file_path)
        try :
            result = predict_image(file_path)
            data['name'] , data ['percentage'] = result
        except Exception as e:
            print(e)
            # # Process your result for human
            data['name'] = ['Error in prediction']
            data['percentage'] = ['Error in prediction']
        print(result)

        os.remove(file_path)
        
        #loop throw data arrays and add to result to array of objects
        result = []
        for i in range(len(data['name'])):
            result.append({
                'name': data['name'][i],
                'percentage': data['percentage'][i]
        })
        #set the data here
        return result
    return None


if __name__ == '__main__':
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    #app.run(threaded=True, port=5000)
    serve(app, host='0.0.0.0', port=port) # <---- ADD THIS
    # try : 
    #     app.run(host='192.168.1.93', port=8000)
    # except :
    #     app.run()
