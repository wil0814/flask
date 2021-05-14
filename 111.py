#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import os

print(__file__)
print(os.path.dirname(__file__))
print(os.path.abspath(__file__))
print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))


print( os.path.basename('/root/runoob.txt') )   # 返回文件名
print( os.path.dirname('/root/runoob.txt') )    # 返回目录路径
print( os.path.split('/root/runoob.txt') )      # 分割文件名与路径
print( os.path.join('root','test','runoob.txt') )
