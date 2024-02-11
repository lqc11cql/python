# @雒启超21009201071
# 解释器

import parser
import math
import turtle
import numpy as np


class Interpreter():
    def __init__(self, path):
        self.MidCode = parser.Parser(path).analyze()
        # 初始化画布
        turtle.setup(width=1.0, height=1.0)
        turtle.penup()

    def create(self):
        # 解析中间代码
        for i in self.MidCode:
            # 操作每一次画图
            for T in np.arange(i[3][0], i[3][1], i[3][2]):
                x = eval(i[4][0])*i[1][0]
                y = eval(i[4][1])*i[1][1]
                x_rot = x * math.cos(i[2])+y*math.sin(i[2])+i[0][0]
                y_rot = y * math.cos(i[2])-x*math.sin(i[2])+i[0][1]
                turtle.goto(x_rot, y_rot)
                turtle.dot()
        turtle.done()

