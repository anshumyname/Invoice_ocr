import cv2
import numpy as np
import constants as cn
from pathlib import Path
from pytesseract import pytesseract
pytesseract.tesseract_cmd = cn.tesseract_path

filename=cn.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_write= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_write,"Pages")

refPt = []
cropping = False



def manual_extraction():
    print("<<<<---Manual Field Extraction Enabled--->>>")
    print("1.Select a field by drawing a rectangle around it")
    print("2.Enter a name for the field and hit enter ")
    print("3. Repeat above for more fields and press q to exit when done")
    img=cv2.imread(str(Path.joinpath(path_to_read,"page1.jpg")))
    imk=img.copy()
    imk= cv2.resize(imk,(int(imk.shape[1]/2),int(imk.shape[0]/2)))
    clone= img.copy()
    custom_config = r"--oem 3 --psm 6"
    texts=[]
    def read(img):
        te=pytesseract.image_to_string(img,config=custom_config)
        return te

    def crop_and_read(event,x,y,flags,params):
        global refPt, cropping
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(2*x, 2*y)]
            cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            refPt.append((2*x, 2*y))
            cropping = False
            cv2.rectangle(imk, (refPt[0][0]//2,refPt[0][1]//2),(refPt[1][0]//2,refPt[1][1]//2), (0, 255, 0), 2)
            roi= clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            gettext= read(roi)
            print(gettext)
            print("-"*10,"Enter a title for selected field ----------")
            name= input() 
            print("-"*10,"Saved")
            texts.append(np.array([name,gettext]))
            
    cv2.namedWindow("Image")
    cv2.setMouseCallback('Image',crop_and_read)
    while(True):
        cv2.imshow('Image',imk)
        key = cv2.waitKey(1) & 0xFF

        if key== ord('q'):
            cv2.destroyAllWindows()
            break
    return np.array(texts)