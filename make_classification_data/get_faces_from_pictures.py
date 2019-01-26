import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("/home/zack/total/python_scripts/make_classification_data/haarcascade_frontalface_default.xml")

write_dir = "/home/zack/Pictures/Ishihara_Satomi/write_dir"
read_dir = "/home/zack/Pictures/Ishihara_Satomi/raw"


import os
if not os.path.exists(write_dir):
    os.makedirs(write_dir)
index = 1
files = os.listdir(read_dir)
for file in files:
    if not os.path.isdir(file):
        img = cv2.imread(os.path.join(read_dir, file))
        if img is not None :
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = img[y:y + h, x:x + w]
                    roi_color=cv2.resize(roi_color, (160, 160), interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(os.path.join(write_dir, str(index)+".jpg"), roi_color)
                    cv2.imshow("face", roi_color)
                    cv2.waitKey(1)
                    index += 1


            except:
                print("something wrong with the picture")
cv2.destroyAllWindows()
