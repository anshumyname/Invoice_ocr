import os
import constants
import numpy as np
from PIL import Image
from pytesseract import Output
from pytesseract import pytesseract
pytesseract.tesseract_cmd = constants.tesseract_path
import cv2
print("Running pytesseract -- version "+ str(pytesseract.get_tesseract_version()))

scaleX = 0.6
scaleY = 0.6
filename= constants.filename
path_to_write= os.getcwd()+"/Details/"+filename+"/Intermediates"
def run_tesseract():
    test= cv2.imread(path_to_write+'/Image_bin.jpg')

    for i in range(3,4):
        print("*"*50)
        # test = cv2.imread('C:/Users/sriva/Documents/Codeblocks_progs/ocr/Output/'+str(i)+'.png')
        #---SCALE AND FILTER
        # test= cv2.resize(test, None, fx= scaleX*3, fy= scaleY*3, interpolation= cv2.INTER_LINEAR)
        # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # test = cv2.filter2D(test, -1, kernel)

        #---------DENOISING 
        test =cv2.bitwise_not(test,mask=None)
        # test = cv2.fastNlMeansDenoisingColored(test,None,10,10,7,21)
        # im_bw = cv2.threshold(np.float32(im), 117, 255, cv2.THRESH_BINARY)[1]
        #(_,test) = cv2.threshold(test, 128, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        #-----ADAPTIVE THRESHOLD
        # test =cv2.adaptiveThreshold(test,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

        
        # cv2.dilate(test, (5, 5), test)
        # cv2.imwrite('sample.jpg',test)
        # cv2.imshow('window',test)
        # cv2.waitKey(0)
        # print("====="+str(i)+"=====")
        # cv2.imwrite('input.jpg',test)
        
        custom_config = r"--oem 3 --psm 4 -c tessedit_create_hocr=1"
        te=pytesseract.image_to_string(test,config=custom_config)
        # xml_input = open("output_hocr1.hocr","r",encoding="utf-8")
        # soup = bs4.BeautifulSoup(xml_input,'lxml')
        # ocr_lines = soup.findAll("span", {"class": "ocr_line"})
        # #We will save coordinates of line and the text contained in the line in lines_structure list
        # lines_structure = []
        # for line in ocr_lines:
        #     line_text = line.text.replace("\n"," ").strip()
        #     title = line['title']
        #     #The coordinates of the bounding box
        #     x1,y1,x2,y2 = map(int, title[5:title.find(";")].split())
        #     lines_structure.append({"x1":x1,"y1":y1,"x2":x2,"y2":y2,"text": line_text})

        # # print(lines_structure)
        

        # # text= pytesseract.image_to_string(test,config='-c preserve_interword_spaces=1')
        # n_boxes = len(lines_structure)
        
        # for c in range(n_boxes):
        #     (x, y, x2, y2) = (lines_structure[c]['x1'],lines_structure[c]['y1'],lines_structure[c]['x2'],lines_structure[c]['y2'])
        #     print(lines_structure[c]['text'])
        #     print()
        #     test = cv2.rectangle(test, (x, y), (x2, y2), (0, 0, 0), 2)
        # print(txt)
        # print(type(te))
        # print(te)
        # cv2.imshow('img', test)
        # cv2.waitKey(0)

        
        with open(path_to_write+'/output.txt','w') as f:
            f.write(str(te))
