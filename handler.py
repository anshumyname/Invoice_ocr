import cv2
import constants as cn
from pathlib import Path

filename=cn.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_write= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_write,"Pages")

def get_cordinates():
    
    def printcoords(event,xs,ys,flags,params):
        #outputting x and y coords to console
        if event==cv2.EVENT_LBUTTONDBLCLK:
            old_x= 3*xs
            oldy_y= 3*ys
            cn.cords.append([old_x,oldy_y])
            print ("Cordinates saved as ",old_x,oldy_y)
    
    imk=cv2.imread(str(Path.joinpath(path_to_read,"page1.jpg")))
    imk= cv2.resize(imk,(int(imk.shape[1]/3),int(imk.shape[0]/3)))
    # cv2.imshow('P
    cv2.namedWindow("Image")
    cv2.setMouseCallback('Image',printcoords)
    while(True):
        cv2.imshow('Image',imk)
        key = cv2.waitKey(1) & 0xFF
        if key== ord('q'):
            break
    cv2.destroyAllWindows()
    