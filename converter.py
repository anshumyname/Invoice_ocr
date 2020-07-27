import pdf2image
import cv2
from pdf2image import convert_from_path

import os

def convert_to_jpeg(pdf_path,output_folder):
    print("converting.......")
    pages = convert_from_path(pdf_path, 500)
    i=0
    for page in pages:
        i+=1
        page.save(output_folder+'/page'+str(i)+'.jpg', 'JPEG')
def in_jpeg(img_path,output_folder):
    img=cv2.imread(img_path)
    cv2.imwrite(output_folder+'/page'+str(i)+'.jpg',img)

if __name__=='__main__':
    convert_to_jpeg('./example/Sample6.pdf','./Intermediates')