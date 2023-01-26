import zipfile
from PIL import Image, ImageOps, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')


parsedImgDic = {}
with zipfile.ZipFile('readonly/images.zip', 'r') as z:
    for entry in z.infolist():
        with z.open(entry) as file:
            img = Image.open(file).convert('RGB')
            parsedImgDic[entry.filename] = {'pil_img':img}
            
for img in parsedImgDic.keys():
    open_cv_image = np.array(parsedImgDic[img]['pil_img']) 
    img2 = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
    faceBox = face_cascade.detectMultiScale(img2, 1.5, 5)
    parsedImgDic[img]['face'] = []
    for x,y,w,h in faceBox:
        face = parsedImgDic[img]['pil_img'].crop((x,y,x + w,y + h))
        parsedImgDic[img]['face'].append(face)
        
for img in parsedImgDic.keys():
    text = pytesseract.image_to_string(parsedImgDic[img]['pil_img'])
    parsedImgDic[img]['text'] = text
        
for img in parsedImgDic.keys():
    for face in parsedImgDic[img]['face']:
        face.thumbnail((150, 150),Image.ANTIALIAS)
        
def search(term):
    for img in parsedImgDic:
        if (term in parsedImgDic[img]['text']):
            print("Result found in file {}".format(img))
            if(len(parsedImgDic[img]['face']) > 0):
                h = int(len(parsedImgDic[img]['face'])/5) + 1
                contactSheet=Image.new('RGB',(600, 150 * h))
                x = 0
                y = 0
                for i in parsedImgDic[img]['face']:
                    contactSheet.paste(i, (x, y))
                    if x + 150 == contactSheet.width:
                        x = 0
                        y += 150
                    else:
                        x += 150
                        
                display(contactSheet)
            else:
                print("There were no faces in that file")
