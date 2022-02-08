from flask import Flask, session, request, send_file
import json
import sys
import os
import zipfile
import shutil
from sys import platform

sys.path.append('../')
from utils import *
import envReader
if not platform == 'win32':
    from detectorTrainer import train
from detector import detector

sys.path.append('../capturers/')
from browser import run
from videoCapturer import detect_from_video

app = Flask('editor')

video_types = [ 'mp4', 'wmv', 'avi', 'avchd', 'flv', 'mkv', 'mov', 'mpeg', 'mpg', 'm4v', 'webm', 'vob', 'ogv', 'ogg', 'drc', 'gif', 'gifv', 'mng']
image_types = [ 'jpg', 'jpeg', 'png', 'pdf', 'tiff', 'gif', 'eps', 'svg', 'ai', 'psd', 'raw', 'bmp', 'ppm', 'pgm', 'pbm', 'pnm', 'webp']

@app.route('/', methods=['POST', 'GET', 'DELETE'])
def main_page():
    if request.method == 'GET':
        return read_file('main.html')
    elif request.method == 'DELETE':
        return json.dumps({'success':False}), 404, {'ContentType':'application/json'}
    elif request.method == 'POST':
        return json.dumps({'success':False}), 404, {'ContentType':'application/json'}

@app.route('/trainer', methods=['POST', 'GET'])
def trainer_page():
    if request.method == 'GET':
        html = read_file('main.html')
        html += '<br><br><center>'
        if platform == 'win32':
            html += 'Trainer is not supported on windows currently!'
        else:
            html += '<form action="/trainer" method="post" id="train" enctype = "multipart/form-data">'
            html += '<label for="client">File Name:</label><br>'
            html += '<input type="text" id="file_name" name="file_name" value=""><br><br>'
            html += '<input type="file" name="file"><br><br>'
            html += '<input type="submit" name="train" value="Train">'
            html += '</form>'
        html += '</center>'
        return html
    elif request.method == 'POST':
        if platform == 'win32':
            return 'invalid OS'
        file_name = request.form['file_name'].strip()
        f = request.files['file']
        if not f.filename.endswith('.zip'):
            return 'only zip files allowed!'
        
        path = './data' + str(f.filename)
        if os.path.exists(path):
            os.remove(path)
            
        f.save(path)
        
        if os.path.exists('./data/' + str(file_name)):
            shutil.rmtree('./data/' + str(file_name))
            
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall('./data/' + str(file_name))
                    
        os.remove(path)
        
        train('./data/' + str(file_name))
        return 'file uploaded succssefully'

@app.route('/detector', methods=['POST', 'GET'])
def detector_page():
    if request.method == 'GET':
        html = read_file('main.html')
        html += '<br><br><center>Supported File Types:<br>'
        html += 'Video: ' + str(video_types) + '<br>'
        html += 'Image: ' + str(image_types) + '<br>'
        html += '<form action="/detector" method="post" id="detect" enctype = "multipart/form-data">'
        html += '<input type="file" name="file"><br><br>'
        html += '<input type="submit" name="detect" value="Detect">'
        html += '</form>'
        html += '</center>'
        return html 
    elif request.method == 'POST':
        if 'detect' in request.form:
            f = request.files['file']
            file_type = getFileType(f.filename)
            if file_type == 'unknown':
                return 'file type not found!'
            
            
            path = './data' + str(f.filename)
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists(path):
                os.rename('./data/' + str(f.filename) + 'result.jpg')
                
            f.save(path)
        
            if (file_type == 'video'):
                detect_from_video(path, video_callback)
            elif (file_type == 'image'):
                d = detector('../resnet50_coco_best_v2.1.0.h5')
                d.detect(loadImgToArray(path), output_image_path='./data/' + str(f.filename) + 'result.jpg', image_callback=image_callback)
            
            return 'file uploaded succssefully'    

def browser_callback(path):
    print(path)

def video_callback(frame, videoName, i):
    d = detector('../resnet50_coco_best_v2.1.0.h5')
    d.detect(frame, output_image_path='./data/' + str(videoName + str(i) + '.jpg'), image_callback=image_callback)
       
def image_callback(path):
    print('path: ', path)
    
def getFileType(file_name):
    for x in video_types:
        if file_name.endswith(x):
            return 'video'
        
    for x in image_types:
        if file_name.endswith(x):
            return 'image'
        
    return 'unknown'
 
if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')
        
    envReader.read('../.env')
    app.run(host=envReader.getValue('EditorIP'), port=envReader.getValue('EditorPort'))