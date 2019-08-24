#!/usr/bin/env python
# -*- coding:utf-8 -*-

__auther__ = 'Jinyang Shao'

import socket
import time
import robot
import test
import process


def Ball_chasing(sock, addr):
    print 'chasing ball'
    print 'Begin recieving data from %s:%s' % addr

    ser, nums = test.all_set_init()
    rob1 = robot.Robot(ser, nums)  # 获取初始坐标
    print 'initial location:'
    rob1.showDegree()
    rob1.move_to(robot.Robot.standloca)  # 机器人初始化
    sock.send('Ready2')  # 对客户端要求使用追踪球体

    try:
        while True:
            data = sock.recv(1024)
            print 'receive :%s' % data
            if data == 'end':
                break
            data = data.decode()
            x, y, z = process.ball_3D(data)
            print 'X= %d Y = %d Z = %d' % (x, y, z)
            rob1.process_data(x, y, z)
    except StandardError:
        sock.close()
    rob1.move_to(robot.Robot.standloca)


def gesture(sock):
    ser, nums = test.all_set_init()
    rob1 = robot.Robot(ser, nums)  # 获取初始坐标
    print 'initial location:'
    rob1.showDegree()
    rob1.move_to(robot.Robot.standloca)  # 机器人初始化
    sock.send('Ready1')
    while True:
        data = sock.recv(1024)
        data = data.decode()
        if not data or data == 'allover':  # 客户端主动结束 sended by handfunc
            print 'terminated by client!'
            sock.send('quit'.encode())
            return 0
        elif data == '2':
            return 0
        elif data == '5':  # 5 根手指追球
            return 1
        elif data == '10':  # 10 根手指追脸
            return 2


def face_chasing(sock, addr):
    print 'Face recongnize and chasing'
    print 'Begin recieving data from %s:%s' % addr
    ser, nums = test.all_set_init()
    rob1 = robot.Robot(ser, nums)  # 获取初始坐标
    print 'initial location:'
    rob1.showDegree()
    rob1.move_to(robot.Robot.standloca)  # 机器人初始化
    sock.send('Ready3')
    try:
        while True:
            data = sock.recv(1024)
            print 'receive  :%s' % data
            if data == 'end':
                break
            data = data.decode()
            x, y = process.face_data(data)
            rob1.process_data(x, y, 0)
    except StandardError:
        print 'error'
        sock.close()
    rob1.move_to(robot.Robot.standloca)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    IP = socket.gethostbyname(hostname)
    print 'this computer\'s ip:%s' % IP
    port = 40005
    s.bind((IP, port))
    # s.close()
    s.listen(1)
    print 'Waiting for function choosing connection...'
    sock, addr = s.accept()
    print 'Begin recieving data from %s:%s' % addr

    while True:
        func_num = gesture(sock)
        print 'gesture return %d' % func_num
        if func_num == 1:  # 5个手指，进行球体追踪
            print 'Waiting for 2D camera connection'
            Ball_chasing(sock, addr)
        elif func_num == 0:  # 0个手指，退出程序
            break
        elif func_num == 2:  # 10个手指
            print 'face recongnize'
            face_chasing(sock, addr)
        print 'Continue to gesture recognize'
    sock.close()

# success
'''
    print 'Waiting for connection...'
    sock, addr = s.accept()
    print 'Waiting for 2D camera connection'
    Ball_chasing(sock, addr)
    sock.close()
'''
# success
'''
    print 'Waiting for 2D camera connection'
    face_chasing(sock, addr)
    sock.close()
'''
'''
    print 'Welcome to gesture based control robot!'
    while True:
        # choice = gesture()
        choice = raw_input('======please input function number:======\n1: chasing ball\n2: chasing ball 3D\n3: face recongnize')
        if choice == '1':
            Ball_chasing()
        elif choice == 'Q':
            break
'''
