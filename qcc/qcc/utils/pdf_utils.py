
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfFileReader

#校验pdf是否有效
from qcc.spiders import const


def check_pdf(pdf_path):
    is_valid = True
    try:
        reader = PdfFileReader(pdf_path)
        if reader.getNumPages() < 1:  # 进一步通过页数判断。
            is_valid = False
    except:
        is_valid = False
    return is_valid

#将多个图片合并成PDF
def product_pdf(out_pdf_name, img_names):
    cover = Image.open(img_names[0])
    width, height = cover.size
    pdf = FPDF(unit="pt", format=[width, height])
    for page in img_names:
        pdf.add_page()
        pdf.image(page, 0, 0)
    pdf.output(out_pdf_name, "F")