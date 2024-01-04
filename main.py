
import glob
import os
import time
import cv2
from mail import *

video = cv2.VideoCapture(0)
time.sleep(1)
initial_frame = None
status_list = []
count = 1


def delete_files():
    images = glob.glob("Images/*.png")
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # parameters = (frame, blur number in tuple form, videocapture )

    if initial_frame is None:
        initial_frame = gray_frame_gau

    delta_frame = cv2.absdiff(initial_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 77, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("my video", dil_frame)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 15000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rect.any():
            status = 1
            cv2.imwrite(f"images/img{count}.png", frame)
            count = count + 1
            all_image = glob.glob("images/*.png")
            index = int(len(all_image) / 2)
            image_object = all_image[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        print(image_object)
        send_mail(message=image_object)
        delete_files()
    cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()