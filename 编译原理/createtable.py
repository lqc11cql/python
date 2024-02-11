# @雒启超21009201071
import math

TOKEN = {
    # 常量
    'PI': {'TYPE': 'CONST_ID', 'VALUE': 'math.pi', 'FUNCTION': None},
    'E': {'TYPE': 'CONST_ID', 'VALUE': 'math.e', 'FUNCTION': None},
    # 变量
    'T': {'TYPE': 'SYMBOL', 'VALUE': None, 'FUNCTION': None},
    # 函数
    'SIN': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.sin'},
    'COS': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.cos'},
    'TAN': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.tan'},
    'LN': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.log'},
    'EXP': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.exp'},
    'SQRT': {'TYPE': 'FUNC', 'VALUE': None, 'FUNCTION': 'math.sqrt'},
    # 保留字
    'ORIGIN': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'SCALE': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'ROT': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'IS': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'FOR': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'FROM': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'TO': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'STEP': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    'DRAW': {'TYPE': 'KEYWORD', 'VALUE': None, 'FUNCTION': None},
    # 运算符
    '+': {'TYPE': 'OP', 'VALUE': None, 'FUNCTION': None},
    '-': {'TYPE': 'OP', 'VALUE': None, 'FUNCTION': None},
    '*': {'TYPE': 'OP', 'VALUE': None, 'FUNCTION': None},
    '/': {'TYPE': 'OP', 'VALUE': None, 'FUNCTION': None},
    '**': {'TYPE': 'OP', 'VALUE': None, 'FUNCTION': None},
    # 记号
    '(': {'TYPE': 'MARK', 'VALUE': None, 'FUNCTION': None},
    ')': {'TYPE': 'MARK', 'VALUE': None, 'FUNCTION': None},
    ',': {'TYPE': 'MARK', 'VALUE': None, 'FUNCTION': None},
    # 结束符
    ';': {'TYPE': 'END', 'VALUE': None, 'FUNCTION': None},
    # 空
    '': {'TYPE': 'EMPTY', 'VALUE': None, 'FUNCTION': None},
    # 数字
    '0': {'TYPE': 'NUMBER', 'VALUE': 0.0, 'FUNCTION': None},
    '1': {'TYPE': 'NUMBER', 'VALUE': 1.0, 'FUNCTION': None},
    '2': {'TYPE': 'NUMBER', 'VALUE': 2.0, 'FUNCTION': None},
    '3': {'TYPE': 'NUMBER', 'VALUE': 3.0, 'FUNCTION': None},
    '4': {'TYPE': 'NUMBER', 'VALUE': 4.0, 'FUNCTION': None},
    '5': {'TYPE': 'NUMBER', 'VALUE': 5.0, 'FUNCTION': None},
    '6': {'TYPE': 'NUMBER', 'VALUE': 6.0, 'FUNCTION': None},
    '7': {'TYPE': 'NUMBER', 'VALUE': 7.0, 'FUNCTION': None},
    '8': {'TYPE': 'NUMBER', 'VALUE': 8.0, 'FUNCTION': None},
    '9': {'TYPE': 'NUMBER', 'VALUE': 9.0, 'FUNCTION': None},
    '.': {'TYPE': 'NUMBER', 'VALUE': None, 'FUNCTION': None},
}

