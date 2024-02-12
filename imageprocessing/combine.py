from pathlib import Path
import sys
import os
import cv2
import json
import time

import smtplib
from email.message import EmailMessage

names = ["people", "fire"]
files = ["yolov5s.pt.json", "['fire.pt'].json"]

def email_alert(subject, to, numPeople):
    msg = EmailMessage()
    msg.set_content("A fire has been detected with " + str(numPeople) + " people around!")
    msg['subject'] = subject
    msg['to'] = to

    user = "flameainotifications@gmail.com"
    msg['from'] = user
    password = "mfdcailizcqtyyim"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

detectedFireOrSmoke = []
detectedSmoke = False
detectedFire = False
filterSec = 3
addedToThisLoopCycle = False
sentFireMessage = False
while True:
    numOfPeople = 0
    confidence = 0
    publish_data = {}
    try:
        detectedSmoke = False
        addedToThisLoopCycle = False
        detectedFire = False
        img = cv2.imread("../curframe.png")
        for file in files:
            with open(file) as json_file:
                data = json.load(json_file)
                if len(data) != 0:
                        for datum in data:
                            c1 = (datum["xyxy"][0], datum["xyxy"][1])
                            c2 = (datum["xyxy"][2], datum["xyxy"][3])
                            if datum["label"].split()[0] in ["person", "Fire", "smoke"]:
                                if (datum["label"].split()[0]) in ["Fire"]:
                                    detectedFireOrSmoke.append(True)
                                    detectedFire = True
                                    confidence = float(datum["label"].split()[1])
                                elif (datum["label"].split()[0]) in ["smoke"]:
                                    detectedSmoke = True
                                else:
                                    detectedFireOrSmoke.append(False)
                                    numOfPeople += 1
                                if len(detectedFireOrSmoke) >= filterSec / 0.01 and not(addedToThisLoopCycle):
                                    del detectedFireOrSmoke[0]
                                    addedToThisLoopCycle = True
                                img = cv2.rectangle(img, c1, c2, datum["colors"], 2)
                                img = cv2.putText(img, datum["label"], (c1[0], c1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, datum["colors"], 2)
        cv2.imwrite("../output.png", img)
        time.sleep(0.01)
    except Exception as e:
        continue
    publish_data["detectedSmoke"] = detectedSmoke
    publish_data["detectedFire"] = detectedFire
    publish_data["numOfPeople"] = numOfPeople
    publish_data["confidence"] = confidence

    with open("output.json", "w") as f:
        json.dump(publish_data, f)
        
    if not(sentFireMessage) and detectedFireOrSmoke.count(True) >= ((filterSec / 0.01) / 2):
        sentFireMessage = True
        email_alert("Fire Alert", "5109800215@vtext.com", numOfPeople)
        email_alert("Fire Alert", "rishita.dhalbisoi@gmail.com", numOfPeople)
        email_alert("Fire Alert", "2403709017@txt.att.net", numOfPeople)
        email_alert("Fire Alert", "saraanshwadkar@gmail.com", numOfPeople)