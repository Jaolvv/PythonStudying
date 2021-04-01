#!/usr/bin/env python 
# -*- coding:utf-8 -*-

"""
# @Time    : 4/1/2021 10:02 AM
# @Author  : 焦虑烧麦
# @File    : 随机产生两个两位整数计算其和差商.py
# @说明/注释:
        1随机产生两个数
        2交换ab位置，使减法不会出现符数
        3用一个变量存储正确的计算结果
        4判断计算结果是否正确
        5用for循环10次
        6在for循环外设置一个变量来储存猜测正确次数
"""
import random

count = 0
# 循环十次
for i in range(10):
    a = int(random.randint(0, 100))  # 随机整数范围0~100
    b = int(random.randint(0, 100))

    # 交换变量，使大数始终在前面
    if a < b:
        b, a = a, b

    count_a = a + b  # 存放+正确的计算结果
    print(str(a) + ' + ' + str(b) + ' = ', end='')
    enter_a = eval(input())

    count_b = a - b  # 存放-正确的计算结果
    print(str(a) + ' - ' + str(b) + ' = ', end='')
    enter_b = eval(input())

    count_c = a * b  # 存放*正确的计算结果
    print(str(a) + ' * ' + str(b) + ' = ', end='')
    enter_c = eval(input())

    if count_a == enter_a:
        print(str(a) + ' + ' + str(b) + ' = ' + str(enter_a) + '√', end='' + " ")
        count += 1
    else:
        print(str(a) + ' + ' + str(b) + ' = ' + str(enter_a) + 'X', end='' + " ")

    if count_b == enter_b:
        print(str(a) + ' - ' + str(b) + ' = ' + str(enter_b) + '√', end='' + " ")
        count += 1
    else:
        print(str(a) + ' - ' + str(b) + ' = ' + str(enter_b) + 'X', end='' + " ")

    if count_c == enter_c:
        print(str(a) + ' * ' + str(b) + ' = ' + str(enter_c) + '√')
        count += 1
    else:
        print(str(a) + ' * ' + str(b) + ' = ' + str(enter_c) + 'X')

print("作答30次,答题正确： " + str(count) + "次")
