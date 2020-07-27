import cv2
import constants
import numpy as np
from PIL import Image
import os
from pytesseract import pytesseract
pytesseract.tesseract_cmd = constants.tesseract_path

filename=constants.filename
path_to_write= os.getcwd()+"/Details/"+filename
def get_data():
    print("----Getting tables-----")
    vert= cv2.imread(path_to_write+'/Intermediates/verticle_lines.jpg')
    actual=cv2.imread(path_to_write+'/Intermediates/Image_bin.jpg')
    actual =cv2.bitwise_not(actual,mask=None)
    ar= np.array(vert);
    height,width,channel= ar.shape

    color=ar[0][0]
    xi=None 
    xj=None
    flag=0
    for i in range(height):
        c=0
        for j in range(0,width,5):
            comp= (ar[i][j]!=color)
            if(comp.all()):
                c+=1
            if c>4:
                xj=i    
            if c>6 and flag==0:
                xi=i
                flag=1
                break
        

    print(xi)
    print(xj)

    # xi=427
    # xj=2259
    dist=[]
    for j in range(0,width):
        mid=(xi+xj)//2
        color=[0,0,0]
        comp= (ar[mid][j]!=color)
        if(comp.all()):
            dist.append(j)

    # print(dist)

    # for k in dist:
        # actual=cv2.line(actual,(k,0),(k,height),(0,255,255),3)
    vert_lines=[]

    cnt=0
    for i in range(1,len(dist)):
        if (dist[i]-dist[i-1])>8:
            if cnt==0: 
                vert_lines.append(dist[i-1])
                cnt+=1
            vert_lines.append(dist[i])
            


    w=width
    h=100
    # img= actual[k:k+h,:]
    # actual=cv2.resize(actual,(800,960))
    # cv2.imshow("sdfe",actual)
    # cv2.waitKey(0)
    n=len(vert_lines)
    total_length=vert_lines[n-1]-vert_lines[0]
    tables=[]
    print(vert_lines)
    m=0
    k=xi
    heading=True
    while k+h<xj:
        # print('***'*39)
        img= actual[k:k+h,:]
        cv2.imwrite(path_to_write+'/Rows/row'+str(m)+'.jpg',img)
        custom_config = r"--oem 3 --psm 3"
        # pytesseract.run_tesseract("rows/row"+str(m)+".jpg","output_hocr1",extension='jpg', lang=None,config=custom_config)
        text= pytesseract.image_to_string(path_to_write+"/Rows/row"+str(m)+".jpg", lang=None,config=custom_config)
        m+=1
        k+=h
        if(len(str(text))<10): continue
        # print(text)
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
        # s=""
        # n_boxes = len(lines_structure)
        # for c in range(n_boxes):
        #     s+=(lines_structure[c]['text'])
        text=(str(text))
        if heading:
            heading=False
            text=text.replace(" ","|")
            text=text.split("|")
            colnames=[]
            for name in text:
                if len(name)>1:
                    colnames.append(name) 
            tables.append(colnames)
            continue
        text=text.replace("|"," ")
        text=text.split()
        # print(text)
        
        splitted=[text[0]]
        txt_len=len(text)
        x=1
        for i in range(2,3):
            ratio=(vert_lines[i]-vert_lines[i-1])/total_length
            t= round(ratio*txt_len)
            end=min(x+t+1,len(text)-1)
            splitted.append(" ".join(text[x:end]))
            x=end
        for i in range(x,len(text)):
            if len(text[i])>1:
                splitted.append(text[i])
        if len(splitted)>3:
            tables.append((splitted))
    
    wid= max([len(i) for i in tables])
    tables= pad(tables,wid,"Null")
    return np.array(tables)

def pad(array,wid, fill_value):
    # dimensions = wid
    for row in array:
        if len(row)<wid:
            for x in range(wid-len(row)) :
               row.append(fill_value)
    
    return array
