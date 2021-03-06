import os
from PIL import Image, ImageDraw
import numpy as np
import cv2
import pickle


faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_alt2.xml")
base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'Faces')
faces_dict = {}
train_faces = []
train_labels = []
counter = 0
size = (550, 550)

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith("jpg"):
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path))
            print(label, "@", path)
            image = Image.open(path).convert("L") # "L" pentru grayscale
            image_mat = np.array(image, "uint8")
            faces = faceCascade.detectMultiScale(image_mat, minNeighbors=4, scaleFactor=1.3) #type: list
            if len(faces) > 1:
                print("file: ", file, " Contains more than one face")
                continue


            if label not in faces_dict:
                faces_dict[label] = counter
                counter -= -1

            id_ = faces_dict[label]
            for (x,y,w,h) in faces:
                face = image_mat[y:y+h, x:x+w]
                train_faces.append(face)
                train_labels.append(id_)

print(faces_dict)
with open("Resources/faces.rick", "wb") as f:
    pickle.dump(faces_dict, f)

reco = cv2.face.LBPHFaceRecognizer_create()
reco.train(train_faces, np.array(train_labels))
reco.save("Resources/face_trainer.yml")
print("end")