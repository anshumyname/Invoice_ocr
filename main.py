import os
from pathlib import Path
import converter, constants,run_ocr, preproces, extraction , tables,converter
from tkinter import Tk, Entry, Frame, LabelFrame, Label, Button, END
import numpy as np
import xlsxwriter

#Making directories for new file 
filename=constants.filename
cur_path= Path.cwd()
p= Path("example") 
read_path= Path.joinpath(p,filename)
joined_path= Path.joinpath(cur_path,"Details")
joined_path= Path.joinpath(joined_path,filename)
try:
    Path.mkdir(joined_path)
    print("------Directory "+filename+ " Created----------")
except OSError as er:
    print("-----Directory for "+filename+" detected----------")
try:
    Path.mkdir(Path.joinpath(joined_path,'Pages'))
    Path.mkdir(Path.joinpath(joined_path,'Intermediates'))
    Path.mkdir(Path.joinpath(joined_path,'Rows'))
except OSError as er:
    print("-----Directory for "+filename+" detected----------")

file_input= Path.joinpath(cur_path,read_path)
file_output= Path.joinpath(joined_path,"Pages")    


#If the format is in pdf then convert it to jpegs
if filename.split(".")[-1]=="pdf":
    converter.convert_to_jpeg(file_input,file_output)
else:
    converter.in_jpeg(file_input,file_output)


page= Path("Pages")
#Process page 1
one = Path.joinpath(page,"page1.jpg")

#Generating binary images and doing morphological operations
preproces.process(Path.joinpath(joined_path,one))

#Run dry tesseract on page to get output.txt
run_ocr.run_tesseract()

#Once output.txt generated extract nominal details from it
buyer=np.array([])
seller=np.array([])
invoice=np.array([])
if constants.manual_field_enable:
    buyer= extraction.get_details()
else:
    buyer, seller, invoice= extraction.get_details()

#Getting the tabular data of the invoice
array= tables.get_data()

#Displaying the extracted data in the GUI with tkinter
root = Tk()

# keep track of widgets
seller_tk = np.empty(seller.shape, dtype=object)
buyer_tk = np.empty(buyer.shape, dtype=object)
invoice_tk = np.empty(invoice.shape, dtype=object)
array_tk = np.empty(array.shape, dtype=object)

# top frame ----------
topframe = Frame(root)
topframe.pack()

# seller details
frame0 = LabelFrame(topframe, text="seller details")
frame0.grid(row=0, column=0)
rows = seller.shape[0]
for i in range(rows):
    l = Label(frame0, text=seller[i][0])
    l.grid(row=i, column=0)
    seller_tk[i][0] = l
    e = Entry(frame0)
    e.grid(row=i, column=1)
    e.insert(END, seller[i][1])
    seller_tk[i][1] = e

# buyer details
frame1 = LabelFrame(topframe, text="buyer details")
frame1.grid(row=0, column=1)
rows = buyer.shape[0]
for i in range(rows):
    l = Label(frame1, text=buyer[i][0])
    l.grid(row=i, column=0)
    buyer_tk[i][0] = l
    e = Entry(frame1)
    e.grid(row=i, column=1,ipadx=10)
    e.insert(END, buyer[i][1])
    buyer_tk[i][1] = e

# invoice details
frame2 = LabelFrame(topframe, text="invoice details")
frame2.grid(row=0, column=2)
rows = invoice.shape[0]
for i in range(rows):
    l = Label(frame2, text=invoice[i][0])
    l.grid(row=i, column=0)
    invoice_tk[i][0] = l
    e = Entry(frame2)
    e.grid(row=i, column=1)
    e.insert(END, invoice[i][1])
    invoice_tk[i][1] = e


# bottom frame ----------
# insert table into the grid
bottomframe = LabelFrame(root, text="transactions")
bottomframe.pack()
rows = array.shape[0]
cols = array.shape[1]
for i in range(rows):
    for j in range(cols):
        e = Entry(bottomframe)
        e.grid(row=i, column=j)
        e.insert(END, array[i][j])
        array_tk[i][j] = e

# functions
# generate xls file from the data in present in tk entries

path_to_write= joined_path
def genxlsx():
    workbook = xlsxwriter.Workbook(Path.joinpath(path_to_write,"Invoice.xlsx"))
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    max_row = 0
    for i in seller_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
    max_row = max(max_row, row)
    row = 0
    col += 6
    for i in buyer_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
        max_row = max(max_row, row)
    row = 0
    col += 6
    for i in invoice_tk:
        worksheet.write(row, col, i[0].cget('text'))
        worksheet.write(row, col+1, i[1].get())
        row += 1
    max_row = max(max_row, row)
    row = max_row + 2
    col = 0
    for i in array_tk:
        for j in i:
            worksheet.write(row, col, j.get())
            col += 1
        col = 0
        row += 1
    workbook.close()


# buttons
buttons = Frame(root)
buttons.pack()
gen = Button(buttons, text="GENERATE", fg="green", command=genxlsx)
gen.grid(row=0, column=0)
quit = Button(buttons, text="QUIT", fg="red", command=root.destroy)
quit.grid(row=0, column=1)

print("==========EXTRACTION FINISHED============")
# mainloop
root.mainloop()
