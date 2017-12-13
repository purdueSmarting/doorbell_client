import cv2
import picamera
from picamera.array import PiRGBArray
import requests
import numpy
import time
import datetime
import json
import io
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_DOWN)

while True:

    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(320, 240))

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    yj_face_cascade = cv2.CascadeClassifier('cascade.xml')

    mem_cnt = 0 # 찍힌 사람의 수
    pic_cnt = 0 # 사진 찍은 횟수
    yj_cnt = 0
    pictures = []

    #time.sleep(1)

    print ("Waiting for pressing the button... ")
    pin = GPIO.wait_for_edge(17, GPIO.FALLING, timeout=5000)

    if pin is None:
        print("Timeout occured!")
        camera.close()
        continue

    print ("Check the button! ")

    current_time = str(datetime.datetime.now())

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

         image = frame.array

         if pic_cnt < 10:
              gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
              gray = cv2.equalizeHist(gray)
              faceList = face_cascade.detectMultiScale(gray, 1.1, 5)

              for(x, y, w, h) in faceList:
                   mem_cnt = mem_cnt + 1
                   pictures.append(image)

              pic_cnt = pic_cnt + 1



         elif pic_cnt == 10:

              for picture in pictures:
                   gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
                   gray = cv2.equalizeHist(gray)
                   picList = yj_face_cascade.detectMultiScale(gray, 1.1, 2, 0, (100, 100), (130,130))

                   #print ("find me!! " + str(len(picList)))

                   if(len(picList) != 0):
                        yj_cnt = yj_cnt + 1

                   for (x, y, w, h) in picList:
                        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 3, 4, 0)

                   cv2.imwrite('result.jpg', image)

              #print ("yj_cnt: " + str(yj_cnt))

              percent = yj_cnt / 10 * 100
              str_per = str(percent)
              info = ''

              #print ("info: " + str(yj_cnt) + ", percent: " + str(percent))
              if percent > 20:
                   info = "Young Ji"
              else:
                   info = "Stranger"

              payload = {'ispressed': int('1'), 'time': current_time, 'visitor': info, 'accuracy': str_per}
              jsonString = json.dumps(payload)
              print(jsonString)
              requests.post('http://13.59.174.162:7579/ispressed', data=payload) # amazon server
              print("request posted")

              camera.close()
              break

         rawCapture.truncate(0)
