import cv2
import constants
import numpy as np
from PIL import Image
from pathlib import Path
from pytesseract import pytesseract
pytesseract.tesseract_cmd = constants.tesseract_path

filename=constants.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_write= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_write,"Intermediates")
def get_data():
    print("----Getting tables-----")
    vert= cv2.imread(str(Path.joinpath(path_to_read,'verticle_lines.jpg')))
    actual=cv2.imread(str(Path.joinpath(path_to_read,'Image_bin.jpg')))
    actual =cv2.bitwise_not(actual,mask=None)
    ar= np.array(vert);
    height,width,channel= ar.shape

    color=ar[0][0]
    xi=None 
    xj=None
    flag=0
    for i in range(height):
        c=0
        for j in range(140,width,5):
            comp= (sum(ar[i][j])>20)
            if(comp):
                c+=1
            if c>6:
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
        comp= sum(ar[mid][j])>20
        if(comp):
            dist.append(j)

    # print(dist)

    # for k in dist:
        # actual=cv2.line(actual,(k,0),(k,height),(0,255,255),3)
    vert_lines=[]
    horizontal_lines=[]
    cnt=0
    for i in range(1,len(dist)):
        if (dist[i]-dist[i-1])>8:
            if cnt==0: 
                vert_lines.append(dist[i-1])
                cnt+=1
            vert_lines.append(dist[i])
    for i in range(xi,xj):
        mid= (vert_lines[0]+vert_lines[-1])//2
        if sum(ar[i][mid])>20:
            horizontal_lines.append(i)

    hts=[]
    for i in range(1,len(horizontal_lines)):
        hts.append(horizontal_lines[i]-horizontal_lines[i-1])

    w=width
    h=100
    if len(hts)>1:
        h=int(hts[1])
    print(h)
    # img= actual[k:k+h,:]
    # actual=cv2.resize(actual,(800,960))
    # cv2.imshow("sdfe",actual)
    # cv2.waitKey(0)
    n=len(vert_lines)
    # print(vert_lines)
    total_length=vert_lines[n-1]-vert_lines[0]
    tables=[]
    
    m=0
    k=xi
    heading=True
    while k+h<xj:
        # print('***'*39)
        img= actual[k:k+h,:]
        r= Path.joinpath(path_to_write,"Rows")
        im_no="row"+str(m)+'.jpg'
        cv2.imwrite(str(Path.joinpath(r,im_no)),img)
        custom_config = r"--oem 3 --psm 3"
        # pytesseract.run_tesseract("rows/row"+str(m)+".jpg","output_hocr1",extension='jpg', lang=None,config=custom_config)
        text= pytesseract.image_to_string(str(Path.joinpath(r,im_no)), lang=None,config=custom_config)
        m+=1
        k+=h
        if(len(str(text))<10): continue
        
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
    tables= pad(tables,wid,"NULL")
    return np.array(tables)

def pad(array,wid, fill_value):
    # dimensions = wid
    for row in array:
        if len(row)<wid:
            for x in range(wid-len(row)) :
               row.append(fill_value)
    
    return array

# x=get_data()

