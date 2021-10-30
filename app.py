import os
import requests
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, request, send_from_directory
from classifier import *
import cv2


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/success', methods=['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'uploads')

    if request.method == 'POST':

        if request.files:
            file = request.files['file']

            if file and allowed_file(file.filename):

                img_path = os.path.join(target_img, file.filename)
                file.save(img_path)
                img = cv2.imread(img_path)

                if request.form['submit_button'] == "Blur all faces":

                    face_boxes = detect_all_faces(img_path)
                    blurred_img = blur_faces(img, face_boxes)
                    img_filename = 'blurred.jpg'
                    cv2.imwrite(os.path.join('static/blurred',  img_filename), blurred_img)

                elif request.form['submit_button'] == "Blur child faces":

                    face_boxes = detect_child_faces(img_path)
                    blurred_img = blur_faces(img, face_boxes)
                    img_filename = 'blurred.jpg'
                    cv2.imwrite(os.path.join('static/blurred', img_filename), blurred_img)

            else:
                error = "Please upload images of .jpg , .jpeg, .jfif and .png extension only."

            if len(error) == 0:
                return render_template('success.html', img=img_filename)
            else:
                return render_template('index.html', error=error)

    if request.form:
        url = request.form.get('link')
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img_path = os.path.join(target_img, 'img_from_link.jpg')
            img.save(img_path)
            img = cv2.imread(img_path)

            if request.form['submit_button'] == "Blur all faces":

                face_boxes = detect_all_faces(img_path)
                blurred_img = blur_faces(img, face_boxes)
                img_filename = 'blurred.jpg'
                cv2.imwrite(os.path.join('static/blurred', img_filename), blurred_img)

            elif request.form['submit_button'] == "Blur child faces":

                face_boxes = detect_child_faces(img_path)
                blurred_img = blur_faces(img, face_boxes)
                img_filename = 'blurred.jpg'
                cv2.imwrite(os.path.join('static/blurred', img_filename), blurred_img)

        except Exception as e:
            print(str(e))
            error = 'This image from this site is not accesible or inappropriate input.'

        if len(error) == 0:
            return render_template('success.html', img=img_filename)
        else:
            return render_template('index.html', error=error)

    else:
        return render_template('index.html')


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=os.getcwd()+"/static/blurred", filename="filename.txt")


if __name__ == "__main__":
    app.run(debug = True)


