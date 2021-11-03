# face-blurring-app


## Description
This app is aimed to automate the process of blurring children faces in images for 
whatever reason it may be. It uses two models: 
* the first one is a face-detector from MTCNN (https://github.com/ipazc/mtcnn) which
is used as it is.
* The second one is a face classification model that predicts if a given face belongs
to a child or an adult. It was trained using aproximately 1000 faces of both classes. 
It uses the xception architecture (https://keras.io/api/applications/xception/) 
with pre-trained weights on imagenet as base model with added dense layers on top.

The app was built on Flask and it takes an image as an input, first detects all faces
and then predicts if each one of the faces belongs to an adult or child. It then blurrs 
faces of children and outputs the blurred image with blurred faces. 
The UI 
![Example Image](/static/blurred/blurred.jpg)

## Installation
If you want to 
