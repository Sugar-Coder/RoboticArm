#!/usr/bin/env python
# -*- coding:utf-8 -*-
__auther__ = "Jinyang Shao"
import re


def ball_2D(center):  # center是个list
    width = 640
    height = 480
    cennums = re.findall(r"\d+", center)
    if len(cennums) != 0:
        x = int(cennums[0])
        y = int(cennums[1])
        return x - width/2, y - height/2
    else:
        return 0, 0
    # return int(center[0]) - 320, int(center[1]) - 240  # 算出重心偏移的坐标


def ball_3D(center):  # center是个3维list，包含深度(记得处理突变数据)
    cennums = re.findall(r"\d+", center)
    if len(cennums) != 0:
        x = int(cennums[0])
        y = int(cennums[1])
        d = int(cennums[2])
        if d == 0:
            dd = 0
        else:
            dd = d - 400
        return x - 320, y - 240, dd
    # 深度可以监测到300 - 800
    else:
        return 0, 0, 0


def face_data(center):
    cennums = re.findall(r"\d+", center)
    if len(cennums) >= 2:
        x = int(cennums[0])
        y = int(cennums[1])
        return x - 320, y - 240
    else:
        return 0, 0