# import tesserocr
import pytesseract
from PIL import Image
import time
from selenium import webdriver

# driver = webdriver.Chrome(r'chromedriver(1).exe')
# driver.set_window_size(2000,1000)
#
# driver.get('http://www.chictr.org.cn/searchproj.aspx')
# n = 1
# while True:
#     n += 1
#     driver.get('http://www.chictr.org.cn/searchproj.aspx?&page=%s'%n)
#     time.sleep(10)
def read_text(text_path):
    """
    传入文本(jpg、png)的绝对路径,读取文本
    :param text_path:
    :return: 文本内容
    """
    # 验证码图片转字符串
    im = Image.open(text_path)
    # 转化为8bit的黑白图片
    imgry = im.convert('L')
    # 二值化，采用阈值分割算法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # 识别文本
    text = pytesseract.image_to_string(out, lang="eng", config='--psm 6')
    return text

if __name__ == '__main__':
    print(read_text(r"D://photo/yzm2.png"))