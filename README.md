# Face Blurring App


## Description
This app is aimed to automate the process of blurring children faces in images for 
whatever reason it may be. It uses two models: 
* The first one is a face-detector from MTCNN (https://github.com/ipazc/mtcnn) which
is used as it is.
* The second one is a face classification model that predicts if a given face belongs
to a child or an adult. It uses the xception architecture 
(https://keras.io/api/applications/xception/) with pre-trained weights on imagenet as
base model with some dense-batchNormalization-dropout layers on top. The full 
architecture of this classification model looks like this: 
![architecture image](/static/architecture.png)

The full training notebook can be seen [here](https://github.com/lucasbegue/face-blurring-app/blob/master/training/training.ipynb)


The app was built on Flask and it takes an image as an input, first detects all faces
and then predicts if each one of the faces belongs to an adult or child. It then blurrs 
faces of children and outputs the blurred image with blurred faces. 
The UI looks like this: 
![UI image](/static/exampleUI.png)
and an example output looks like this:
![Example Image](/static/blurred/blurred.jpg)

## Using the app
If you want to run the app locally first clone the repo:
`git clone https://github.com/lucasbegue/face-blurring-app.git`
and then run on shell:
```
cd face-blurring-app
pyhon app.py
```
and you will have the app running locally.


