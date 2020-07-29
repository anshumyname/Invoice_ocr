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
    horzt= cv2.imread(str(Path.joinpath(path_to_read,'horizontal_lines.jpg')))
    actual=cv2.imread(str(Path.joinpath(path_to_read,'Image_bin.jpg')))
    actual =cv2.bitwise_not(actual,mask=None)
    ar= np.array(vert);
    ahr= np.array(horzt)
    height,width,channel= ar.shape
    
    color=ar[0][0]
    xi=None 
    xj=None
    flag=0
    for i in range(height):
        c=0
        for j in range(20,width,5):
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
    for j in range(0,width,6):
        mid=(xi+xj)//2
        # print(ar[mid][j])
        comp= sum(ar[mid][j])>20
        if(comp):
            dist.append(j)

    # print(dist)
     
    # for k in dist:
        # actual=cv2.line(actual,(k,0),(k,height),(0,255,255),3)
    vert_lines=dist
    horizontal_lines=[]
    # cnt=0
    # for i in range(1,len(dist)):
    #     if (dist[i]-dist[i-1])>8:
    #         if cnt==0: 
    #             vert_lines.append(dist[i-1])
    #             cnt+=1
    #         vert_lines.append(dist[i])
    for i in range(xi,xj+1,5):
        mid= (vert_lines[0]+vert_lines[-1])//2
        if sum(ahr[i][mid])>20:
            horizontal_lines.append(i)
    
    #==============UNCOMMENT TO SEE THE VERTICAL AND HORIZONTAL LINES=============
    # mid= (vert_lines[0]+vert_lines[-1])//2
    # imk= cv2.line(actual,(mid,0),(mid,height),(0,255,0),10)
    # imk=actual
    # for ho in horizontal_lines:
    #     imk= cv2.line(imk,(0,ho),(width,ho),(255,0,0),10)
    # for vo in vert_lines:
    #     imk= cv2.line(imk,(vo,0),(vo,height),(255,0,0),10)
    #  cv2.imwrite(str(Path.joinpath(path_to_read,"tables_lens.jpg")),imk)
    # read= cv2.imread('mix.jpg')
    # read= cv2.resize(read,(1080,720))
    # cv2.imshow('ime',read)
    # cv2.waitKey(0)

    w=width
    h=100
    # img= actual[k:k+h,:]
    # actual=cv2.resize(actual,(800,960))
    # cv2.imshow("sdfe",actual)
    # cv2.waitKey(0)
    n=len(vert_lines)
    print(vert_lines)
    print(horizontal_lines)
    total_length=vert_lines[n-1]-vert_lines[0]
    tables=[]
    for i in range(len(horizontal_lines)-1):
        text=[]
        for j in range(len(vert_lines)-1):
            x=horizontal_lines[i]
            y=vert_lines[j]
            w=vert_lines[j+1]-vert_lines[j]
            h=horizontal_lines[i+1]-horizontal_lines[i]
            img=actual[x:x+h,y:y+w]
            r= Path.joinpath(path_to_write,"Rows")
            im_no="row"+str(i+j)+'.jpg'
            cv2.imwrite(str(Path.joinpath(r,im_no)),img)
            custom_config = r"--oem 3 --psm 6"
            # pytesseract.run_tesseract("rows/row"+str(m)+".jpg","output_hocr1",extension='jpg', lang=None,config=custom_config)
            txt= pytesseract.image_to_string(str(Path.joinpath(r,im_no)), lang=None,config=custom_config)
            text.append(str(txt))
        tables.append(text)
    
    # m=0
    # k=xi
    # heading=True
    
    # # print('***'*39)
    # img= actual[k:k+h,:]
    
    # m+=1
    # k+=h
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

