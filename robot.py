#!/usr/bin/env python
# -*- coding:utf-8 -*-

__auther__ = 'Jinyang Shao'

import test
import re
import time
import math

class Robot(object):

    step = 5
    ax = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    limit = [140, 165, 180, 90, 180, 180, 58]
    Rlimit = []
    standloca = [15, 90, 65, 60, 60, 80, 58]

    def __init__(self, ser, nums):  # 7维轴，G是爪子
        self.ser = ser
        self.__axis = nums

    def closeser(self):
        self.ser.close()

    def showDegree(self):
        print 'A:%s B:%s C:%s D:%s E:%s F:%s G:%s' % (self.__axis[0], self.__axis[1], self.__axis[2], self.__axis[3], self.__axis[4], self.__axis[5], self.__axis[6])

    # 直接对串口输入数据
    def single_move(self, command):
        res = test.command_check(command)
        if res != 'Command ERROR' and res != 'HELP' and res != 'QUIT':
            self.ser.write(command.encode())
            ans = self.ser.readline(40)
            print ("arduino return :%s" % ans)
        else:
            print 'ERROR command check the syntax!'

# 步长为step的加减
    def add(self, axis, step=0):  # 加2,axis传入大写轴字母,之前判断完是否达到极限值
        if step == 0:
            step = Robot.step
        command = "ADD "
        command = command + axis
        command = command + " "
        command = command + str(step)

        self.ser.write(command.encode())
        s = self.ser.readlines(40)
        change = re.findall(r"\d+", s[1])
        # print '%s to %s' % (change[0], change[1])
        if len(change) >= 2:
            nowaxis = int(change[1])
        else:
            nowaxis = -1

        if nowaxis != -1:
            if axis == 'A':
                self.__axis[0] = nowaxis
            elif axis == 'B':
                self.__axis[1] = nowaxis
            elif axis == 'C':
                self.__axis[2] = nowaxis
            elif axis == 'D':
                self.__axis[3] = nowaxis
            elif axis == 'E':
                self.__axis[4] = nowaxis
            elif axis == 'F':
                self.__axis[5] = nowaxis
            elif axis == 'G':
                self.__axis[6] = nowaxis

    def minus(self, axis, step=0):
        if step == 0:
            step = Robot.step
        command = "MINUS "
        command = command + axis
        command = command + " "
        command = command + str(step)
        self.ser.write(command.encode())
        # print 'minus respond:'
        s = self.ser.readlines(40)
        change = re.findall(r"\d+", s[1])
        # print '%s to %s' % (change[0], change[1])
        if len(change) >= 2:
            nowaxis = int(change[1])
        else:
            nowaxis = -1
        if nowaxis != -1:
            if axis == 'A':
                self.__axis[0] = nowaxis
            elif axis == 'B':
                self.__axis[1] = nowaxis
            elif axis == 'C':
                self.__axis[2] = nowaxis
            elif axis == 'D':
                self.__axis[3] = nowaxis
            elif axis == 'E':
                self.__axis[4] = nowaxis
            elif axis == 'F':
                self.__axis[5] = nowaxis
            elif axis == 'G':
                self.__axis[6] = nowaxis

    def set(self, axis, dire):
        command = 'SET '
        command = command + axis
        command = command + ' '
        command = command + str(dire)
        self.ser.write(command.encode())
        # print 'minus respond:'
        s = self.ser.readlines(40)
        change = re.findall(r"\d+", s[1])
        # print '%s to %s' % (change[0], change[1])
        nowaxis = int(change[1])
        if axis == 'A':
            self.__axis[0] = nowaxis
        elif axis == 'B':
            self.__axis[1] = nowaxis
        elif axis == 'C':
            self.__axis[2] = nowaxis
        elif axis == 'D':
            self.__axis[3] = nowaxis
        elif axis == 'E':
            self.__axis[4] = nowaxis
        elif axis == 'F':
            self.__axis[5] = nowaxis
        elif axis == 'G':
            self.__axis[6] = nowaxis

    # 重新更新各个角度
    def getdegree(self, type=0):
        if type != 0:
            return [self.__axis[0], self.__axis[1], self.__axis[2], self.__axis[3], self.__axis[4], self.__axis[5], self.__axis[6]]
        command = "SHOW DEGREE"
        self.ser.write(command.encode())
        s = self.ser.readlines(40)
        nums = re.findall(r"\d+", s[1])
        nums = map(int, nums)
        # print nums
        self.__axis = nums

    # 移动到newa轴数组所在的坐标位置
    def move_to(self, newa):
        if len([j for j in range(len(newa)) if newa[j] > Robot.limit[j]]) != 0:  # 对于超过界限的不予操作
            print '超过界限！'
            return
        while len([i for i in range(len(newa)) if self.__axis[i] != newa[i]]) != 0:
            index = [k for k in range(len(newa)) if self.__axis[k] != newa[k]]  # 提取值不等的下标
            for ind in index:
                if abs(self.__axis[ind] - newa[ind]) < Robot.step:  # 对于小于步长无法调整的，直接归等
                    self.set(Robot.ax[ind], newa[ind])
                    # newa[ind] = self.__axis[ind]
                elif self.__axis[ind] < newa[ind]:
                    self.add(Robot.ax[ind])
                elif self.__axis[ind] > newa[ind]:
                    self.minus(Robot.ax[ind])
                else:
                    continue

    def goRight(self, speed='M'):  # F 减，distance以cm为单位
        '''
        RF = 18
        if self.__axis[5] <= 90:  # 在第一象限
            away = int(RF * math.sin(math.radians(90 - self.__axis[5])) + distance)
            print 'sin : %d' % math.sin(math.radians(90 - self.__axis[5]))
            print 'away:%d F axis:%d' % (away, self.__axis[5])
            if away > RF:
                self.set('F', 0)
                return
            else:
                newax = int(90 - math.asin(away/RF))
        else:  # 在第三象限
            away = int(RF * math.sin(math.radians(self.__axis[5] - 90)) - distance)
            if away >= 0:  # 机械臂保留在第三象限
                self.set('F', int(math.asin(math.radians(away/RF))))  # 如果后期发现速度太快，则改正
                return
            else:  # 需要移动到第二象限
                self.set('F', 90)
                newax = int(90 - math.asin(math.radians((abs(away))/RF)))
        new_axis_set = self.getdegree(1)
        new_axis_set[5] = newax
        self.move_to(new_axis_set)
        '''
        if speed == 'L':
            step = 3
        elif speed == 'M':
            step = 5
        else:
            step = 8
        if self.__axis[5] - step > 0:
            self.minus('F', step)
        else:
            self.set('F', 0)
        self.add('D', int(step/2))  # 也可能是减，具体下次实验测量

    def goLeft(self, speed='M'):  # F 加
        '''
        RF = 18  # 同样需要根据B轴角度计算
        if self.__axis[5] >= 90:  # 当机械臂在第三象限的时候
            away = RF * math.sin(self.__axis[5] - 90) + distance
            if away > RF:  # 移动距离超出半径
                self.set('F', 180)
                return
            else:
                newax = int(90 + math.asin(away/RF))
        else:  # 当机械臂在第二象限时 0<F<90
            away = RF * math.sin(90 - self.__axis[5]) - distance
            if away >= 0:  # 移动不超出第一象限
                self.set('F', int(90 - math.asin(away/RF)))
                return
            else:  # 移动到到第三象限
                newax = int(90 + math.asin(abs(away)/RF))
        step = 4
        while self.__axis[5] != newax:
            if newax - self.__axis[5] > step:
                self.add('F', step)
            else:
                self.set('F', newax)
        '''
        if speed == 'L':
            step = 3
        elif speed == 'M':
            step = 5
        else:
            step = 8
        if self.__axis[5] + step < Robot.limit[5]:
            self.add('F', step)
        else:
            self.set('F', Robot.limit[5])
        self.minus('D', int(step/2))  # 也可能是减，具体下次实验测量

    def goUp(self, speed='M'):  # A 减
        steplimit = self.__axis[0]  # A 轴可以减小到的最小角度 A - 0
        if speed == 'L':
            step = 2
        elif speed == 'M':
            step = 4
        else:
            step = 8
        if step > steplimit:
            step = steplimit
        self.minus('A', step)

    def goDown(self, speed='M'):  # A加
        if self.__axis[1] >= 70:  # B轴大于九十度
            Alimit = 140 - self.__axis[1]  # A 最大角度 140 - B
        elif self.__axis[1] >= 60:
            Alimit = 65
        elif self.__axis[1] >= 50:
            Alimit = 70
        elif self.__axis[1] >= 40:
            Alimit = 60
        elif self.__axis[1] >= 30:
            Alimit = 50
        elif self.__axis[1] >= 20:
            Alimit = 45
        else:
            Alimit = 30
        if speed == 'L':
            step = 2
        elif speed == 'M':
            step = 4
        else:
            step = 7
        if step + self.__axis[0] < Alimit:
            self.add('A', step)
        else:
            self.set('A', Alimit)

    def goForward(self, speed='M'):  # B 减
        if speed == 'L':
            step = 2
        elif speed == 'M':
            step = 4
        else:
            step = 8
        if self.__axis[1] - step > 0:
            self.minus('B', step)
        else:
            self.set('B', 20)

    def goBackward(self, speed='M'):  # B 加
        if speed == 'L':
            step = 2
        elif speed == 'M':
            step = 4
        else:
            step = 8
        if self.__axis[1] + step < 140:
            self.add('B', step)
        else:
            self.set('B', 140)

    def process_data(self, x, y, d):  # 传入偏移量
        if abs(x) < 30 and abs(y) < 40 and abs(d) < 20:
            return
        # dir = ''
        if d != 0:
            if 5 < abs(d) < 40:  # 深度控制
                if d > 0:
                    # dir = dir + 'Forward '
                    self.goForward('L')
                else:
                    # dir = dir + 'Backward '
                    self.goBackward('L')
            elif 40 <= abs(d) < 70:
                if d > 0:
                    # dir = dir + 'Forward '
                    self.goForward('M')
                else:
                    # dir = dir + 'Backward '
                    self.goBackward('M')
            elif abs(d) >= 70:
                if d > 0:
                    # dir = dir + 'Forward '
                    self.goForward('H')
                else:
                    # dir = dir + 'Backward '
                    self.goBackward('H')
        # 水平调整
        if abs(x) < 80:
            if x > 0:
                # dir = dir + 'goRight '
                self.goRight('L')
            else:
                # dir = dir + 'goLeft '
                self.goLeft('L')
        elif abs(x) < 120:
            if x > 0:
                # dir = dir + 'goRight '
                self.goRight('M')
            else:
                # dir = dir + 'goLeft'
                self.goLeft('M')
        elif abs(x) < 150:
            if x > 0:
                # dir = dir + 'goRight'
                self.goRight('H')
            else:
                # dir = dir + 'goLeft'
                self.goLeft('H')
        elif abs(x) >= 150:
            if x > 0:
                self.goRight('M')
                self.goRight('H')
            else:
                self.goLeft('M')
                self.goLeft('H')
        # 高低调整
        if 40 < abs(y) < 80:
            if y > 0:
                # dir = dir + 'goDown '
                self.goDown('L')
            else:
                # dir = dir + 'goUp '
                self.goUp('L')
        elif 80 <= abs(y) < 140:
            if y > 0:
                # dir = dir + 'goDown '
                self.goDown('M')
            else:
                # dir = dir + 'goUp '
                self.goUp('M')
        elif abs(y) >= 140:
            if y > 0:
                # dir = dir + 'goDown '
                self.goDown('H')
            else:
                # dir = dir + 'goUp'
                self.goUp('H')

'''
ser, nums = test.all_set_init()
rob1 = Robot(ser, nums)  # 获取初始坐标
print 'initial location:'
rob1.showDegree()
# rob1.single_move('SET A 60')
print 'moving...'
#             A    B   C  D   E   F   G
rob1.move_to(Robot.standloca)

command = raw_input('D :Right  A :Left  W :Up  S :down  Q:Forward  E:Backward stdl: go to std loca\n>>>')
while True:
    if command == 'w':
        rob1.goUp()
    elif command == 's':
        rob1.goDown()
    elif command == 'a':
        rob1.goLeft()
    elif command == 'd':
        rob1.goRight()
    elif command == 'q':
        rob1.goForward()
    elif command == 'e':
        rob1.goBackward()
    elif command == 'stdl':
        rob1.move_to(Robot.standloca)
    elif command == 'Q':
        break
    else:
        print 'Wrong input!'
    command = raw_input('D :Right  A :Left  W :Up  S :down  Q:Forward  E:Backward stdl: go to std loca\n>>>')
'''

'''
rob1.goRight('M')
time.sleep(0.5)
rob1.goLeft('H')
rob1.goDown('M')
rob1.goDown('M')
rob1.goUp('M')
rob1.goUp('M')
time.sleep(0.3)
rob1.goForward('M')
time.sleep(0.3)
rob1.goBackward('M')
'''
