#!/usr/bin/env python 
# -*- coding:utf-8 -*-

"""
# @Time    : 3/30/2021 7:20 PM
# @Author  : 焦虑烧麦
# @File    : Temp.py
# @说明/注释: 
"""
import random


# +
def addition():
    a = int(random.randint(0, 100))  # 随机整数范围0~100
    b = int(random.randint(0, 100))

    count_a = a + b  # 存放+正确的计算结果
    print(str(a) + ' + ' + str(b) + ' = ', end='')
    enter = eval(input())
    if enter != count_a:
        print('你的回答：' + str(a) + ' + ' + str(b) + ' = ' + str(enter) + ' ×! 正确结果为：' + str(count_a))
    elif enter == count_a:
        print('你的回答：' + str(a) + ' + ' + str(b) + ' = ' + str(count_a) + ' √')

    count_b = a - b  # 存放-正确的计算结果
    print(str(a) + ' - ' + str(b) + ' = ', end='')
    enter = eval(input())
    if enter != count_b:
        print('你的回答：' + str(a) + ' - ' + str(b) + ' = ' + str(enter) + ' ×! 正确结果为：' + str(count_b))
    elif enter == count_b:
        print('你的回答：' + str(a) + ' - ' + str(b) + ' = ' + str(count_b) + ' √')

    count_c = a * b  # 存放*正确的计算结果
    print(str(a) + ' * ' + str(b) + ' = ', end='')
    enter = eval(input())
    if enter != count_c:
        print('你的回答：' + str(a) + ' * ' + str(b) + ' = ' + str(enter) + ' ×! 正确结果为：' + str(count_c))
    elif enter == count_c:
        print('你的回答：' + str(a) + ' * ' + str(b) + ' = ' + str(count_c) + ' √')


addition()