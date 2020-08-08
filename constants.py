#File to be read
filename="Sample8.pdf"
#Write your tesseract.exe path here
tesseract_path= r'C:\Users\sriva\AppData\Local\Tesseract-OCR\tesseract.exe'
#Enable manual detection for tables
manual_field_enable=False    #Will be True only if it is set to True
manual_table_enable=False    #It will set automatically to True if tables are not detected
#Stores cordinates of tables when labelled manually
cords=[]

