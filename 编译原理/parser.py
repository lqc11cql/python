# @雒启超21009201071
# 语法分析器

import ast
import math
import os

import astunparse

import scanner


class Parser:
    def __init__(self, path):
        # 中间代码生成
        self.state_of_origin = [0, 0]  # 原点默认值
        self.state_of_scale = [1, 1]  # 图像放大默认值
        self.state_of_rot = 0  # 图像旋转默认值
        self.state_of_for = [0, 0, 0]  # 绘图的状态参数
        self.draw = ['', '']  # 画图
        self.MidCode = []
        # 中间代码生成结束
        self.scanner = scanner.Scanner(path)
        self.dataflow = self.scanner.analyze()
        self.pos = 0  # 数据读取位置
        self.length = len(self.dataflow)  # 数据流长度

    def analyze(self):
        while(self.pos < self.length):
            # 匹配保留字
            # S->'ORIGIN'T|'SCALE'T|'ROT'T|'FOR'P
            # T->'IS('E','E')'|'IS'E
            # E为一个算数表达式
            # P为FOR后特殊结构
            if self.dataflow[self.pos][1]['TYPE'] == 'KEYWORD':
                self.output(self.dataflow[self.pos][0])
        # 转换为列表
        return [eval(x) for x in self.MidCode]

    def output(self, string):
        # 输出

        self.pos += 1
        if string == 'ORIGIN':
            self.ORIGIN()
        elif string == 'SCALE':
            self.SCALE()
        elif string == 'ROT':
            self.ROT()
        elif string == 'FOR':
            self.FOR()

            self.MidCode.append(str((self.state_of_origin, self.state_of_scale,
                                     self.state_of_rot, self.state_of_for, self.draw)))
        else:
            raise SyntaxError()

    def ORIGIN(self):
        self.matchstring('IS')
        templist = self.matchparameter()
        # 更改平移状态
        self.state_of_origin[0] = eval(templist[0])
        self.state_of_origin[1] = eval(templist[1])

    def SCALE(self):
        self.matchstring('IS')
        templist = self.matchparameter()
        # 更改缩放状态
        self.state_of_scale[0] = eval(templist[0])
        self.state_of_scale[1] = eval(templist[1])

    def ROT(self):
        self.matchstring('IS')
        # 更改旋转状态
        self.state_of_rot = eval(self.matchexpression())

    def FOR(self):
        self.matchstring('T')
        self.matchstring('FROM')
        # 更改FOR状态
        self.state_of_for[0] = eval(self.matchexpression())
        self.matchstring('TO')
        self.state_of_for[1] = eval(self.matchexpression())
        self.matchstring('STEP')
        self.state_of_for[2] = eval(self.matchexpression())
        self.matchstring('DRAW')
        templist = self.matchparameter()
        # 更改画图状态
        self.draw[0] = templist[0]
        self.draw[1] = templist[1]

    def matchstring(self, string):
        # 匹配一个特定的字符串
        if self.dataflow[self.pos][0] == string:
            self.pos += 1
        else:
            raise SyntaxError()


    def matchparameter(self):
        # 匹配(E,E)
        # 即匹配参数列表
        # 如：
        # ORIGIN IS (5,5);
        # 后面的括号中包括括号的部分都是参数列表
        temp = self.matchexpression()  # 缓冲区
        # 转换为列表[E,E]
        if temp[0] == '(' and temp[-1] == ')':
            temp = temp[1:-1].split(',')
        else:
            raise SyntaxError()
        return temp

    def matchexpression(self):
        # 匹配E或者(E,E)
        # 即匹配一个算数表达式
        # 如
        # 5*2-LN(3)
        # (5*2-3,tan(0.1))
        temp = ''  # 缓冲区
        while(self.dataflow[self.pos][0] != ';' and self.pos < self.length and self.dataflow[self.pos][1]['TYPE'] != 'KEYWORD'):
            if self.dataflow[self.pos][1]['TYPE'] == 'FUNC':
                temp += self.dataflow[self.pos][1]['FUNCTION']
            elif self.dataflow[self.pos][1]['TYPE'] == 'CONST_ID':
                temp += self.dataflow[self.pos][1]['VALUE']
            else:
                temp += self.dataflow[self.pos][0]
            self.pos += 1
        if self.dataflow[self.pos][0] == ';':
            self.pos += 1  # 跳过结尾的分号
        return temp

