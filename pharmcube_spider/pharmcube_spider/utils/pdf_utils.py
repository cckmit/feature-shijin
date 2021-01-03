import os

import pdfkit
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfFileReader
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

#校验pdf是否有效
from pharmcube_spider import run_env


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

#生成PDF
def convert2pdf(pdf_name, html):
    if 'dev' == run_env.run_evn:
        config_pdf = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string('<head><meta charset="UTF-8"> </head>'+html, pdf_name, configuration=config_pdf)
    else:
        pdfkit.from_string('<head><meta charset="UTF-8"> </head>'+html, pdf_name,)

#  pdf_list = [{'pdf_name':'/home/zengxiangxu/temp/test.pdf','html':'<div> ... </div>'}]
def auto_html2pdf(pdf_list):
    # 利用多线程生成PDF
    executor = ThreadPoolExecutor(max_workers=10)  #线程的个数
    # submit()的参数： 第一个为函数， 之后为该函数的传入参数，允许有多个
    future_tasks = [executor.submit(convert2pdf, pdf_name=pdf_info['pdf_name'], html=pdf_info['html']) for pdf_info in pdf_list]
    # 等待所有的线程完成，才进入后续的执行
    wait(future_tasks, return_when=ALL_COMPLETED)

