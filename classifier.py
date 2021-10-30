import numpy as np
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import cv2


detector = MTCNN()
model = load_model('training/models/final_model.h5')


def rescale(img):
    return np.add(np.multiply(img, 2/255), -1)


def detect_all_faces(img_path):
    img = cv2.imread(img_path)
    detections = detector.detect_faces(img)
    boxes = []

    for det in detections:
        boxes.append(det['box'])

    return np.array(boxes)


def detect_child_faces(img_path):
    img = cv2.imread(img_path)
    detections = detector.detect_faces(img)
    faces = []
    boxes = []

    for det in detections:
        boxes.append(det['box'])
        (x, y, w, h) = det['box']
        cropped_face = img[y:y+h, x:x+w]
        cropped_face = cv2.resize(cropped_face, (128, 128))
        cropped_face = rescale(cropped_face)
        faces.append(cropped_face)

    faces = np.array(faces)
    predictions = np.squeeze(model.predict(faces), axis=-1)
    child_indexes = [1 if pred>0.5 else 0 for pred in predictions]
    child_faces = []

    for i in range(len(boxes)):
        if child_indexes[i] == 1:
            child_faces.append(boxes[i])

    return np.array(child_faces)


def blur_faces(img, boxes):
    for box in boxes:
        (x, y, w, h) = box
        face = img[y:y+h, x:x+w]
        face_blurred = blur(face)
        img[y:y+h, x:x+w] = face_blurred
    return img


def blur(img, interpolation=cv2.INTER_NEAREST):
    h, w, _ = img.shape
    ratio = h/w
    h_ = 8
    w_ = int(h_/ratio)
    img_ = cv2.resize(img, dsize=(w_, h_), interpolation=interpolation)
    img_blurred = cv2.resize(img_, dsize=(w, h), interpolation=cv2.INTER_NEAREST)
    return img_blurred

