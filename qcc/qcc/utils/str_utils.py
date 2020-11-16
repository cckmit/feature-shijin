# -*- coding:utf-8 -*-
import re


class StrUtils:

    #将字符串中文符号转换为英文符号
    def cnMark2ENMark(self,str):
        mark = {ord(f): ord(t) for f, t in zip(u'，。！？【】（）％＃＠＆１２３４５６７８９０｛｝；',u',.!?[]()%#@&1234567890{};')}
        return str.translate(mark)


    #判断字符串是否包含数字
    def hasNums(self,str):
        if None == str:
            return False
        return bool(re.search(r'\d', str))

    #提取字符串中的中文
    def get_cn(self,str):
        return re.findall(r'[\u4e00-\u9fa5]', str)

    # 判断字符串是否为空
    def isBlank(self,str):
        if str == None:
            return True
        if str.isspace():
            return True
        if len(str) == 0:
            return True
        return False