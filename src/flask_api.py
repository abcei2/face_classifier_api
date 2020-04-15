import os
import json

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from face_classifier import *


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return all([
        '.' in filename,
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    ])


def is_busy():

    with open('src/database.json', 'r') as json_file:
        data = json.load(json_file)
    if(data['flag_occupied'] == "BUSY"):
        return True
    else:
        with open('src/database.json', 'w') as json_file:
            data['flag_occupied'] = "BUSY"
            json.dump(data, json_file)
        return False


def not_busy():
    with open('src/database.json', 'r') as json_file:
        data = json.load(json_file)

    with open('src/database.json', 'w') as json_file:
        data['flag_occupied'] = "NOT BUSY"
        json.dump(data, json_file)

    print("NOT BUSY")


@app.route('/classify_faces/', methods=['POST'])
def upload_file():
    # check if the post request has the file part

    if is_busy():
        resp = jsonify({'message': 'Service is being used'})
        resp.status_code = 503
        return resp

    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        not_busy()
        return resp

    file_1 = request.files['file']

    if file_1.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        not_busy()
        return resp

    if file_1 and allowed_file(file_1.filename):
        filename = secure_filename(file_1.filename)

        file_1.save(os.path.join("./", filename))
        img = cv2.imread(f"./{filename}")

        detections = do_detect(img)
        print(detections)
        resp = jsonify({'message': detections})
        resp.status_code = 200
        not_busy()
        return resp

    else:
        resp = jsonify({
            'message': f'Allowed file types are {ALLOWED_EXTENSIONS}'
        })
        resp.status_code = 400
        not_busy()
        return resp


@app.route('/delete_images/', methods=['GET'])
def delete_images():
    resp = jsonify({'message': do_delete_images()})
    resp.status_code = 200
    return resp


@app.route('/update_model/', methods=['GET'])
def update_model():

    if is_busy():
        resp = jsonify({'message': 'Service is being used'})
        resp.status_code = 503
        return resp

    do_update()

    resp = jsonify({'message': 'Successfully updated'})
    resp.status_code = 200
    not_busy()
    return resp


@app.route('/register_face/', methods=['POST'])
def register_face():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    try:
        name = json.loads(request.form.get('json', '{}'))["face_name"]
    except KeyError:
        resp = jsonify({'message': 'No face_name in request'})
        resp.status_code = 400
        return resp

    file_1 = request.files['file']
    if file_1.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    if not file_1 or not allowed_file(file_1.filename):
        resp = jsonify({
            'message': f'Allowed file types are {ALLOWED_EXTENSIONS}'
        })
        resp.status_code = 400
        return resp

    filename = secure_filename(file_1.filename)
    file_1.save(os.path.join("./", filename))

    img = cv2.imread(f"./{filename}")
    do_register(img, name)

    resp = jsonify({'message': "Success upload"})
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
