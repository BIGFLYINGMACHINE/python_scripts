import cv2
import dlib
import os
import sys
import random

output_dir = './my_faces'
size = 64

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 改变图片的亮度与对比度
def relight(img, light=1, bias=0):
    w = img.shape[1]
    h = img.shape[0]
    #image = []
    for i in range(0,w):
        for j in range(0,h):
            for c in range(3):
                tmp = int(img[j,i,c]*light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j,i,c] = tmp
    return img


# 打开摄像头 参数为输入流，可以为摄像头或视频文件
camera = cv2.VideoCapture(1)

index = 466
while True:
    if (index <= 5000):  #照片的数量
        face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        print('Being processed picture %s' % index)
        # 从摄像头读取照片
        success, img = camera.read()
        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用detector进行人脸检测
        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
        for(x, y, w, h) in faces:
            face = img[y:y+h, x:x+w]
            # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
            #face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
            face = cv2.resize(face, (size,size))
            cv2.imshow('image', face)
            cv2.imwrite(output_dir+'/'+str(index)+'.jpg', face)
            index += 1
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break
    else:
        print('Finished!')
        break
