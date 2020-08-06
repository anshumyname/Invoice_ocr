from pathlib import Path
import constants
import numpy as np
from PIL import Image
from pytesseract import pytesseract
pytesseract.tesseract_cmd = constants.tesseract_path
import cv2


scaleX = 0.6
scaleY = 0.6
filename= constants.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_read= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_read,"Intermediates")
def run_tesseract():
    print("Running pytesseract -- version "+ str(pytesseract.get_tesseract_version()))
    test= cv2.imread(str(Path.joinpath(path_to_read,'Image_bin.jpg')))

    for i in range(3,4):
        print("*"*50)
        test =cv2.bitwise_not(test,mask=None)
        custom_config = r"--oem 3 --psm 4"
        te=pytesseract.image_to_string(test,config=custom_config)
        with open(Path.joinpath(path_to_read,'output.txt'),'w') as f:
            f.write(str(te))
