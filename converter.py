import pdf2image
from pdf2image import convert_from_path

class Converter :
    @staticmethod
    def convert_to_jpeg(pdf_path,output_folder):
        pages = convert_from_path(pdf_path, 900)
        i=0
        for page in pages:
            i+=1
            page.save(output_folder+'/out'+str(i)+'.jpg', 'JPEG')

if __name__=='__main__':
    conv= Converter()
    conv.convert_to_jpeg('./example/Sample4.pdf','./imgs')