import torch
import torchvision.transforms as transforms
import yaml
import numpy as np
import cv2
from picamera2 import Picamera2
import time
import subprocess
from ultralytics import YOLO
from roboflow import Roboflow
from picamera2 import Picamera2, Preview
from picamera2.previews import QtGlPreview
import time
import json
import subprocess
from gtts import gTTS
import pygame
import re



# Initialize PiCamera2
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.NULL)
picam2.start()

# Load class names from data.yaml
data_yaml_path = "dataset/data.yaml"
with open(data_yaml_path, "r") as file:
    data = yaml.safe_load(file)
class_names = data["names"]

#Model
rf = Roboflow(api_key="KCTLCouvartskFTBdvnj")
project = rf.workspace("object-detection-of-college").project("outdoor-navigation")
model = project.version(1, local="http://localhost:9001/").model

#subprocess.Popen(["python3", "/home/devang/Object_Detection_Files/motion_feedback_360.py"])
#print("Haptic feedback on")

# Main loop for capturing images and performing object detection
try:
    while True:
        time.sleep(1)
        #capture image
        picam2.capture_file("img.jpg")

        #object detectin
        prediction = model.predict("/home/devang/Object_Detection_Files/clearway/pkl_object_detect/img.jpg", confidence=30, overlap=30)
        
        #Storing output + Audio feedback
        for pred in prediction:
            class_name = pred["class"]
            #distance = subprocess.run(["python3", "/home/devang/Object_Detection_Files/distance_calculation.py"])
            distance_output = subprocess.run(["python3", "/home/devang/Object_Detection_Files/distance_calculation.py"], capture_output=True)
            
            distance = distance_output.stdout
            distance_str = distance.decode("utf-8")
            match = re.match(r"Distance: (\d+\.\d+) (\w+)", distance_str)
            numeric_value = match.group(1)
            unit = match.group(2)
            dist_out = (f"{numeric_value}{unit}")
            print(f"Class: {class_name}, distance: {dist_out}")

            #Audio output
            audio_output = (f"{class_name} at {dist_out}")
            tts = gTTS(audio_output)
            tts.save('audio_feedback.mp3')

            #play audio
            pygame.mixer.init()
            pygame.mixer.music.load("audio_feedback.mp3")
            pygame.mixer.music.get_volume()
            #pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            
       

except KeyboardInterrupt:
    pass
finally:
    picam2.close()
