import cv2
import constants, handler
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
    # Reading images
    vert= cv2.imread(str(Path.joinpath(path_to_read,'verticle_lines.jpg')))
    horzt= cv2.imread(str(Path.joinpath(path_to_read,'horizontal_lines.jpg')))
    actual=cv2.imread(str(Path.joinpath(path_to_read,'Image_bin.jpg')))
    actual =cv2.bitwise_not(actual,mask=None)
    ar= np.array(vert)
    ahr= np.array(horzt)
    height,width,channel= ar.shape
    horizontal_lines=[] #Stores the cordinates of horizontal lines
    vert_lines=[]        #Stores the cordinates of vertical lines
    xi=None            # Starting point of the table
    xj=None             #End point of the table
    flag=0
    #Loop over the image to find the xi and xj by count of vertical lines (>4)
    for i in range(height):
        c=0
        for j in range(50,width,3):
            comp= (sum(ar[i][j])>15)
            if(comp):
                c+=1
            if c>4:
                xj=i    
            if c>4 and flag==0:
                xi=i
                flag=1
                break
        
    print("Start",xi)
    print("End", xj)

    
    h=0
    #ENABLED IF HORIZONTAL LINES AREN'T AVAILABLE
    manual=constants.manual_table_enable
    if (xi!=None and xj!=None):
            
            #Get cordinates of horizontal and vertical lines
            for j in range(0,width,3):
                mid=(xi+xj)//2
                comp= sum(ar[mid][j])>10
                if(comp):
                    vert_lines.append(j)
            
            for i in range(xi,xj+1,3):
                mid= (vert_lines[0]+vert_lines[-1])//2
                if sum(ahr[i][mid])>10:
                    horizontal_lines.append(i)

    
    # If cordinates couldn't be be found properly manually it is taken
    if(xi==None or xj==None or len(vert_lines)<=3 or manual):
        print("<<<<<---Image too rough for reading ..Mannual assistance needed-->>>>>>")
        print("1. In the opened image double click to save the cordinates ")
        print("2. First save the starting horizontal line , then line immediate next to that for taking width and finally the end point of table ")
        print("3. Now for vertical lines cordinates double click from left to right all vertical lines starting point ")
        handler.get_cordinates()
        li=constants.cords
        xi=li[0][1]
        xj=li[2][1]
        h=li[1][1]-li[0][1]
        vert_lines=[li[i][0] for i in range(3,len(li))]
        manual=True
    
    #Plotting the saved cordinates 
    imk=np.copy(actual) 
    imk= cv2.line(imk,(0,xi),(width,xi),(55,56,240),5)
    imk= cv2.line(imk,(0,xj),(width,xj),(55,56,240),5)
    for ho in horizontal_lines:
        imk= cv2.line(imk,(0,ho),(width,ho),(255,0,0),5)
    for vo in vert_lines:
        imk= cv2.line(imk,(vo,0),(vo,height),(255,0,0),5)
    
    for i in range(len(horizontal_lines)-1):
        for j in range(len(vert_lines)-1):
            p1=(vert_lines[j],horizontal_lines[i])
            p2=(vert_lines[j+1],horizontal_lines[i+1])
            imk=cv2.rectangle(imk,p1,p2,(55,0,i*20+90),4)    
    cv2.imwrite(str(Path.joinpath(path_to_read,"tables_drawn.jpg")),imk)
    
    tables=[]
    #If we have horizontal lines on the table
    if (manual==False):
        if(abs(horizontal_lines[0]-xi)>10):
            horizontal_lines.insert(0,xi)
        if(abs(horizontal_lines[-1]-xj)>10):
            horizontal_lines.append(xj)
        #Performing box by box extraction 
        rw=0
        for i in range(len(horizontal_lines)-1):
            text=[]
            for j in range(len(vert_lines)-1):
                y=horizontal_lines[i]
                x=vert_lines[j]
                h=vert_lines[j+1]-vert_lines[j]
                w=horizontal_lines[i+1]-horizontal_lines[i]
                img=actual[y:y+w,x:x+h]
                r= Path.joinpath(path_to_write,"Rows")
                im_no="row_"+str(rw)+"_col_"+str(j)+'.jpg'
                cv2.imwrite(str(Path.joinpath(r,im_no)),img)
                custom_config = r"--oem 3 --psm 6"
                # pytesseract.run_tesseract("rows/row"+str(m)+".jpg","output_hocr1",extension='jpg', lang=None,config=custom_config)
                txt= pytesseract.image_to_string(img, lang=None,config=custom_config)
                text.append(txt)
            rw+=1
            tables.append(text)
    else:
        rw=0
        #Performing box by box extraction with fixed width
        for i in range(xi,xj+1,h):
            text=[]
            for j in range(len(vert_lines)-1):
                x=i
                y=vert_lines[j]
                w=vert_lines[j+1]-vert_lines[j]
                img=actual[x:x+h,y:y+w]
                r= Path.joinpath(path_to_write,"Rows")
                im_no="row_"+str(rw)+"_col_"+str(j)+'.jpg'
                
                cv2.imwrite(str(Path.joinpath(r,im_no)),img)
                custom_config = r"--oem 3 --psm 6"
                # pytesseract.run_tesseract("rows/row"+str(m)+".jpg","output_hocr1",extension='jpg', lang=None,config=custom_config)
                txt= pytesseract.image_to_string(str(Path.joinpath(r,im_no)), lang=None,config=custom_config)
                text.append(str(txt))
            rw+=1
            tables.append(text)
    
    #Pad with null values if not in proper format
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



