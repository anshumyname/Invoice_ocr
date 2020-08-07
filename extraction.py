import constants
import numpy as np
from pathlib import Path
import io

#This file reads output.txt line by line and finds if required details can be found inside in it

filename=constants.filename
path_to_read= Path.cwd()
path_to_read= Path.joinpath(path_to_read,"Details")
path_to_read= Path.joinpath(path_to_read,filename)
path_to_read= Path.joinpath(path_to_read,"Intermediates")

def get_details():
    print("----Extracting-------")
    text=[]
    f= open(Path.joinpath(path_to_read,'output.txt'))
    lines= f.readlines()
    for line in lines:
        if len(line)>2:
            text.append(line)
    f.close()
    buyer_details=[]
    seller_details=[]
    invoice_details=[]

    
    if ("INVOICE" in text[0])==False:
        buyer_details.append(np.array(["Name",text[0]]))
    else:
        m=2
        if len(text[1])>4: m=1 
        spl= text[m].split(" ")
        if len(spl[0])>2:
            buyer_details.append(np.array(["Name",spl[0]]))
        else:
            buyer_details.append(np.array(["Name",spl[m]]))

    gst=0
    adresfound=0
    adresindex=None
    adresx=None
    inv=False
    po_found=False
    for line in text:
        if "Invoice" in line:
            idx=line.find("Invoice")
            if inv==False:
                inv=True
                invoice_details.append(["Invoice No.",line[idx+5:]])
            else:
                invoice_details.append(["Invoice Date",line[idx+5:]])

        if ("GSTIN" in line):
            idx=line.find("GSTIN")
            if gst==0:
                take=min(len(line)-1,idx+35) 
                buyer_details.append(np.array(["Buyer_GSTIN",line[idx:take]]))
                gst+=1
            further=line[idx+1:]
            idx2= further.find("GSTIN")
            if gst==1:
                idt=None
                if idx2<len(further): 
                    idt=idx2
                    seller_details.append(np.array(["Seller_GSTIN",further[idt:]]))
                    gst+=1
                else:
                    idt=idx
                    seller_details.append(np.array(["Seller_GSTIN",line[idt:]]))
                    gst+=1
        if ("PO" in line) and po_found==False:
            po_found=True
            idx=line.find("PO")
            invoice_details.append(np.array(["PO_Number",line[idx:]]))
        if ("State") in line:
            idx=line.find("State")
            take=min(len(line)-1,idx+22) 
            seller_details.append(np.array(["Seller_State",line[idx+5:take]]))
        if "Due" in line:
            idx=line.find("Due")
            take=min(len(line)-1,idx+17)
            invoice_details.append(np.array(["Due_date",line[idx+6:take]]))
        if "PAN " in line:
            # print("--------------------------")
            idx=line.find("PAN")
            seller_details.append(np.array(["Seller_Id",line[idx+3:]]))
        if adresfound>0:
            take=0
            if adresindex:
                take=max(0,adresindex)
                seller_details[adresx][1]+=line[take:]
            adresfound-=1    
        if ("ddress" or "shipping" in line) and adresfound>0 :
            idx=line.find("ddress")
            idx2=line[idx+1:].find("ddress")
            idx=max(idx,idx2)
            adresx=len(seller_details)
            seller_details.append(np.array(["Seller_Address",line[idx+6:]]))
            # fields["seller_address"]=line[idx+6:]
            adresfound=2
            adresindex=idx
    return np.array(buyer_details),np.array(seller_details),np.array(invoice_details)
    
    
