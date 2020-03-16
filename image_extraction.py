import subprocess
import sys
import os
import cv2
from datetime import datetime
import flask
import json
from flask import jsonify
from flask import Flask, request
from flask import Response
from flask_cors import CORS
app = flask.Flask(__name__)
cors = CORS(app)


input_dir = sys.argv[1]
output_dir = sys.argv[2]

def shell_call(fileName):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    out_dir = output_dir+"/"+ os.path.basename(fileName)+dt_string
    subprocess.call(["sudo" ,"sh","./img_extract.sh",fileName , out_dir ], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_dir

def extract_image(imagePath):
    #imagePath = sys.argv[1]
    cascPath = "haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    #print("Found {0} faces!".format(len(faces)))
    if len(faces) > 0:
        return True
    else:
        return False 

parsedFiles = []
parsed_results = {}

if os.path.isdir(input_dir):  
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            req = input_dir+'/'+filename
            res = shell_call(req)
            parsedFiles.append(res)
            parsed_results[req] = res
elif os.path.isfile(input_dir):  
    if input_dir.endswith(".pdf"):
        res = shell_call(input_dir)
        parsedFiles.append(res)
        parsed_results[input_dir] = res

FINAL_RESULTS = {}
for k, v in parsed_results.items():
    if os.path.isdir(v):  
        for filename in os.listdir(v):
            if filename.endswith(".jpg"):
                c_dir = v+'/'+filename
                if extract_image(c_dir):
                    #print("Image Content Dir ",c_dir)
                    FINAL_RESULTS[k] = c_dir


                    
print(FINAL_RESULTS)

'''

@app.route('/get_image', methods=['POST'])
def get_image():
    jsonObj = request.get_json(force=True)
    print('Request---> ', jsonObj)
    for k,v in jsonObj.items():
        if k == "input":
            profile_path = v

    res = faceDetection_v1.facial_extraction(profile_path)

   

    json_data = json.dumps(d1)
    return Response(json_data, status=200, mimetype='application/json')

if __name__ =='__main__':
    app.run(host="0.0.0.0",port=int("8005"),debug=True,use_reloader=False)
'''
