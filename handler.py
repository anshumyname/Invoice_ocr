import cv2
import constants as cn
from pathlib import Path

#This file opens the document for manually saving the cordinates of starting and ending points

filename=cn.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_write= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_write,"Pages")

def get_cordinates():
    #Function to print cordinates    
    def printcoords(event,xs,ys,flags,params):
        #outputting x and y coords to console on double click
        if event==cv2.EVENT_LBUTTONDBLCLK:
            old_x= 2*xs
            oldy_y= 2*ys
            cn.cords.append([old_x,oldy_y])
            print ("Cordinates saved as ",old_x,oldy_y)
    
    #Display 1/3rd of the image to have a full look at a time
    imk=cv2.imread(str(Path.joinpath(path_to_read,"page1.jpg")))
    imk= cv2.resize(imk,(int(imk.shape[1]/2),int(imk.shape[0]/2)))
    cv2.namedWindow("Image")
    cv2.setMouseCallback('Image',printcoords)
    while(True):
        cv2.imshow('Image',imk)
        key = cv2.waitKey(1) & 0xFF
        if key== ord('q'):
            break
    cv2.destroyAllWindows()
    