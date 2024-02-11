# @雒启超21009201071
import os
import scanner
import compile

if __name__ == '__main__':
    path = os.getcwd()
    compile.Compile(path+r'\test.txt', path+r'\output1.py').create()


