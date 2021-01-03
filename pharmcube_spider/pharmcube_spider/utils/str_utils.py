# -*- coding:utf-8 -*-
import re

class StrUtils:

    #将字符串中文符号转换为英文符号
    def cn_mark2en_mark(self, str):
        if '' == str or None == str:
            return str
        mark = {ord(f): ord(t) for f, t in zip(u'，。！？【】（）％＃＠＆１２３４５６７８９０｛｝；', u',.!?[]()%#@&1234567890{};')}
        return str.translate(mark)

    #判断字符串是否包含数字
    def has_nums(self, str):
        if None == str:
            return False
        return bool(re.search(r'\d', str))

    #提取字符串中的中文
    def get_cn(self, str):
        return re.findall(r'[\u4e00-\u9fa5]', str)

    #提取字符串中的数字
    def get_num(self, str):
        return re.findall(r"\d+\.?\d*", str)

    # 判断字符串是否为空
    def is_blank(self, str):
        if str == None:
            return True
        if str.isspace():
            return True
        if len(str) == 0:
            return True
        return False

    # 提取英文小括号里面的数据
    def get_parentheses_str(self, str):
        return re.findall(r'(?<=\().*?(?=\))', str)

    # 提取英文中括号里面的数据
    def get_brackets_str(self, str):
        return re.findall(r'(?<=\[).*?(?=\])', str)

    def remove_mark(self, str):
        punctuation = '[’!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~，。,；，【】（）｛｝！《》‘’ ：]'
        return re.sub(punctuation, '', str)

    #将字符串按照标点符号拆分
    def split_mark(self, str):
        return re.findall(r"[\w']+", str)

    #是否以字母开头
    def is_en_start(self, str):
        rule = re.match(r'[a-zA-Z]', str)
        if None == rule:
            return False
        return True

    #是否以数字开头
    def is_nums_start(self, str):
        rule = re.match(r'[0-9]', str)
        if None == rule:
            return False
        return True

    def strip(self, str):
        if None == str:
            return str
        return str.strip()

