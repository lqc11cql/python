# @雒启超21009201071
# 输入处理器
import re

import lexer


class Scanner():
    def __init__(self, path):
        # 读入文件位置
        self.path = path
        # 设置缓冲区
        self.text = ""
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                # 将文件中注释去掉
                self.text = self.text + \
                    line.split("//")[0].split("--")[0].split("\n")[0]
        self.text = self.text.upper().strip()
        self.lexer = lexer.Lexer()
        self.output_lists = []

    def analyze(self):
        sentences = re.split("(;)", self.text)
        # No.0
        # 识别
        # E->E;|ε
        # 用于记录状态机状态,当state == True时,意味着可以读入一个E,当state == False时,意味着可以读入一个;
        state = True
        for sentence in sentences:
            if state and sentence != ";":
                state = False
                self.lexer.getToken(sentence)
                self.output_lists.extend(self.lexer.output_list)
            elif sentence == ";":
                state = True
            else:
                raise SyntaxError()
        if state:
            raise SyntaxError()
        # No.0   识别结束
        return self.output_lists
