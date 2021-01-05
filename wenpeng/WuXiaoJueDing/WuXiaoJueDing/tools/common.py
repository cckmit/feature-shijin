# -*- coding: utf-8 -*- 
import hashlib
import re
import time

from datetime import datetime,timedelta


#def get_md5(content):
#    if isinstance(content, str):
#        content = content.encode("utf-8")
#    m = hashlib.md5()
#    m.update(content)
#    return m.hexdigest()

#def get_md5(self, data):
#    m = hashlib.md5(data.encode())
#    return m.hexdigest()

def get_md5(content):
    m = hashlib.md5(content.encode())
    return m.hexdigest()





#def is_collect(keys,decision_num,application_num,publication_date_new,title,patentee_spidser,invalids_applicant_spidser):
#    if not (decision_num and application_num and publication_date_new,title,patentee_spidser,invalids_applicant_spidser):
#        return False
#    count = 0
#    for i in keys:
#        if i in (decision_num and application_num and publication_date_new,title,patentee_spidser,invalids_applicant_spidser):
#            count += 1
#            break
#    if count > 0:
#        return True
#    else:
#        return False

def is_collect(keys,decision_num,application_num,publication_date_new,title,patentee_spidser,invalids_applicant_spidser):
    if not (decision_num and application_num and publication_date_new and title and patentee_spidser and invalids_applicant_spidser):
        return False
    count = 0
    for i in keys:
        if i in (decision_num and application_num and publication_date_new and title and patentee_spidser and invalids_applicant_spidser):
            count += 1
            break
    if count > 0:
        return True
    else:
        return False


#好像是common.py我改错了，不是逗号，而是 and

def sum_time( ts):
    if '分钟前' in ts:
        a = ts.split('分钟前')[0]
        publish_date = ((datetime.now() - timedelta(minutes=int(a))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif '小时前' in ts:
        b = ts.split('小时前')[0]
        publish_date = ((datetime.now() - timedelta(hours=int(b))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif '天前' in ts:
        c = ts.split('天前')[0]
        publish_date = ((datetime.now() - timedelta(minutes=int(c))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif ts == '刚刚':
        publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        publish_date = datetime.strptime(ts, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M:%S')
    publish_date = int(time.mktime(time.strptime(publish_date, "%Y-%m-%d %H:%M:%S")))
    return publish_date


import os
#方法1.将图片合并到PDF
# from PyPDF2 import PdfFileReader,PdfFileMerger
# from reportlab.lib.pagesizes import A4,landscape,portrait
# from reportlab.pdfgen import canvas
# # pip3 install PyPDF2
# # pip3 install reportlab
# def jpg_to_pdf(img_dir='./images/',pdf_name = 'result1.pdf'):
#     list_jpgs=[os.path.join(img_dir,fn) for fn in os.listdir(img_dir) if fn.endswith('jpeg')]
#     if not list_jpgs:return
#     result_pdf=PdfFileMerger()
#     temp_pdf='temp.pdf'
#     for i in sorted(list_jpgs):
#         cnv=canvas.Canvas(temp_pdf,pagesize=portrait(A4))
#         cnv.drawImage(i,0,0,*portrait(A4))
#         cnv.save()
#         with open(temp_pdf,'rb') as f:
#             pdf_reader=PdfFileReader(f)
#             result_pdf.append(pdf_reader)
#     result_pdf.write(pdf_name)
#     result_pdf.close()
#     if os.path.exists(temp_pdf):os.remove(temp_pdf)


#方法2.将图片合并到PDF
import os
#pip install PyMuPDF
# def pic2pdf(img_dir='./images/', pdf_name='result.pdf'):
#     import fitz
#     import glob
#     [os.removedirs(img_dir+i) for i in os.listdir(img_dir) if not i.endswith('jpeg')]
#     doc = fitz.open()
#     temp_pdf = 'temp.pdf'
#     for img in sorted(glob.glob("{}/*".format(img_dir))):  # 读取图片，确保按文件名排序
#         imgdoc = fitz.open(img)  # 打开图片
#         pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
#         imgpdf = fitz.open("pdf", pdfbytes)
#         doc.insertPDF(imgpdf)  # 将当前页插入文档
#     if os.path.exists(temp_pdf):os.remove(temp_pdf)
#     doc.save(pdf_name)  # 保存pdf文件
#     doc.close()






