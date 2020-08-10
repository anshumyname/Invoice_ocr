##### Levle 3 in Flipkart GRID 2.0 (Electronic Incoicing using Image Processing)
# Invoice OCR
This repo aims to convert scanned invoices to excel sheet using cv2 and pytesseract for reading the invoices. It converts the invoice to binary form and detects horizontal and vertical lines to construct the tabular data and perform tesseract reading on each block. It also generates an output txt file where all the extracted data are placed and named fields can be obtained by searching within it.
It supports both PDFs and Jpegs format.

## Dependencies
- pdf2image [with poppler](https://pypi.org/project/pdf2image/)
- pytesseract (5.0 + ) [Recommended to install from here](https://github.com/tesseract-ocr/tesseract/wiki)

Go ahead with pip install for these three
- cv2 (4.2.0 + )
- numpy
- tkinter
- xlswriter

## How To Use
- Clone the repo on your system
- Install dependencies above
- Place the invoice pdf/jpeg files you want to run ocr in the examples folder
- In the **constatnts.py** file change the **tesseract_path= ""** to the path on your computer where (.../Tesseract-OCR/tesseract.exe) is located
- In the same file write the name of file in **filename=""** which you just placed in example folder. If your file doesn't have horizontal lines set **manuable_enable=True**
- Run **main.py** in cmd
- You'll find all your  results in **Details** folder with a sub-directory of your filename for each input

## WorkFlow and Architechture
The program begins with **main.py** which creates the directory by the name of filename itself for each new file for which the program is run for the first time where it stores all the results. Let the filename on which the program is running be invoice.pdf/jpeg so a invoice.pdf named directory will be created inside Details folder.

Further whole procedure is divided into four steps
#### 1.Transformation
Here if the file is pdf then it is converted to jpeg and then stored in *Details/invoice.pdf/Pages* directory as *page1.jpg*
Otherwise if its already in jpg format its stored directory as *page1.jpg.* All of these process is done in **converter.py**

#### 2.Detection
Second step is to detect text and perform run tesseract on it.
So prior to it the **preproces.py** file will perform some thresholding and morphological transformations for detecting vertial and horizontal lines which will be used later. The images will be stored again in the file directory as *.Details/invoice.pdf/Intermediates/*. 
Then with the processed image stored as Image_bin.jpg we'll run tesseract ocr on it which will be done by **run_ocr.py** file which stores the results as output.txt file.

#### 3. Extraction
Well we have done raw extraction in output.txt file now the **extraction.py** will search for the named fields like *Name,GSTIN, InvoiceNo, PO_Number..* and return it in three arrays buyer_details,seller_details,and invoice_details where coresponding fields are in corresponding array.

After doing fields extraction we'll begin dealing with tables in **tables.py** where we inititally search for start and end point of the table using count of vertical lines .*(table contains more vertcal lines on page than any other section)*. After getting start and end points we'll get cordinates of vertical lines and horizontal lines.

In case the image is too rough for getting cordinates **handler.py** opens the file page in a window for manual assistance.
Here you need to manually store the cordinates by double clicking on the image. First we store horizontal lines (1st ,2nd and last -- line) then we store all vertical lines beginning ( || ). Click **q** to exit when done.

Then after getting cordinates we can split the table into individual boxes and run ocr on it. Each box is stored in *Details/invoice.pdf/Rows* folder.

#### 4.Validation
Now we have all the details the main.py resumes running and opens a GUI where we can see our extracted named fields and the table. All the boxes are editable so if you found something wrond you can edit it instantly. 

If everything is correct press the **"GENERATE"** button to obtain an excel file in "/Details/invoice.pdf/" folder as Invoice.xlsx . Bravo you are done.

## Advantages
- Supports both pdfs/jpeg
- Can deal with variable column length in tables.
- Manual assistance feature enables extracting tables with or without lines.
- If image is properly tabulated and scanned no manual assistance is needed.
- Intermediates and Rows folder to let user see the performance on the given input file.


## Drawbacks
- Doesn't deal with tilted images.
- If the image is too much unclear for tesseract to read then it may output gibberish.
- Fixed Named Fields - Different name for the same namefields aren't captured like 
Shipping Address is captured but not Shipping Details
- If horizontal lines aren't present assumes equal width of rows.


[Github Link To this Repo](https://github.com/anshumyname/Invoice_ocr/tree/testing)



