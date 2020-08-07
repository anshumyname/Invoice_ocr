import cv2
from skimage import io
from pathlib import Path
import constants
import numpy as np

#CONSTANTS
filename=constants.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_read= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_read,"Intermediates")

#Function for displaying an image
def show_wait_destroy(winname, img):
    img= cv2.resize(img, (720,1080))
    cv2.imshow(winname, np.array(img, dtype = np.uint8 ))
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)


#Functon for preprocessing
def process(img_path):
    print("*"*50)
    print("------Reading image--------")
    img = cv2.imread(str(img_path), 0)  # Read the image
    
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin =cv2.bitwise_not(img_bin,mask=None)  # Invert the image

    print("-------Storing binary image--------")
    cv2.imwrite(str(Path.joinpath(path_to_read,"Image_bin.jpg")),img_bin)

    print("-----Applying Morphological Operations-----")
    # Defining a kernel length
    hkernel_length = np.array(img).shape[1]//30
    vkernel_length = hkernel_length#np.array(img).shape[0]//30 
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, hkernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (vkernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dst=img_bin
    

    img_temp1 = cv2.erode(dst, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)

    cv2.imwrite(str(Path.joinpath(path_to_read,"verticle_lines.jpg")),verticle_lines_img) #Storing vertical lines
    ar= np.array(verticle_lines_img)
    
    height,width= ar.shape

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(dst, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite(str(Path.joinpath(path_to_read,"horizontal_lines.jpg")),horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("----------Intermediates_images_saved--------")
    