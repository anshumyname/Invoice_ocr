import cv2
import os
import constants
import numpy as np

filename=constants.filename
path_to_write= os.getcwd()+"/Details/"+filename+"/Intermediates"
def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


#Functon for extracting the box
def box_extraction(img_for_box_extraction_path):

    print("Reading image..")
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    # img= cv2.resize(img,(1080,1080))
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin =cv2.bitwise_not(img_bin,mask=None)  # Invert the image

    print("Storing binary image to Images/Image_bin.jpg..")
    cv2.imwrite(path_to_write+"/Image_bin.jpg",img_bin)

    print("Applying Morphological Operations..")
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//40
     
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dst=img_bin
    # dst =cv2.bitwise_not(dst,mask=None)
    # dst =cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    # kernelone = np.ones((5,5),np.float32)/25
    # dst = cv2.filter2D(dst,-1,kernelone)
    # cv2.imwrite(path_to_write+"/Normal.jpg",dst)
    # cv2.imshow('name',dst)
    # cv2.waitKey(0)
    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(dst, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite(path_to_write+"/verticle_lines.jpg",verticle_lines_img)
    ar= np.array(verticle_lines_img)
    
    height,width= ar.shape

    x= int(0.94*width)
    y1= 0
    y2= height

    # verticle_lines_img= cv2.line(verticle_lines_img,(x,y1),(x,y2),(255,255,255),3)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(dst, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite(path_to_write+ "/horizontal_lines.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("Intermediates_images_saved")
    

    


#Input image path and out folder
# box_extraction("./imgs/out1.jpg")