#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re


def list_ports():
    import serial.tools.list_ports
    print ('========choosing the ports======')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports()), 1):
        print('--- {:2}: {:20} {}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        port = raw_input('--- Enter port index or full name:')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                print ('--- Invalid index!\n')
                continue
        except ValueError:
            print ('Invalid value')
            pass
        else:
            port = ports[index]
        print(port)
        ser = serial.Serial(port, 9600, timeout=1)
        return ser


def initialize():
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print (p.name)
        if p.description.startswith('Arduino 101 Serial Monitor'):
            break
    ser = serial.Serial(p.device, 9600, timeout=1)
    return ser


# 判断输入命令的类型
def command_check(command):
    token_list = command.split()
    if command == 'HELP':
        return 'HELP'
    if command == 'QUIT':
        return 'QUIT'
    elif command == 'SHOW DEGREE':
        return 'SHOW DEGREE'
    elif len(token_list) == 3:
        if token_list[0] not in ['SET', 'ADD', 'MINUS']:
            return 'Command ERROR'
        if token_list[1] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            return 'Command ERROR'
        try:
            int(token_list[2])
        except:
            return 'Command ERROR'
    else:
        return 'Command ERROR'
    return 'VALUE'


def all_set_init():  # 获得初始数据给Robot类
    print('Initialising...')
    try:
        ser = list_ports()
        # ser = initialize()
        print('Initialised')
    except:
        print('Initialise - Failed')
        ser.close()
        return
    command = "SHOW DEGREE"
    # command = "SET A 45"
    ser.write(command.encode())
    s = ser.readlines(40)
    nums = re.findall(r"\d+", s[1])
    nums = map(int, nums)  # 将list转化为int
    return ser, nums

'''
print('Initialising...')
try:
    ser = list_ports()
    print('Initialised')
except:
    print('Initialise - Failed')
    ser.close()
command = "ADD A 1"
# command = "SET A 45"
ser.write(command.encode())
s = ser.readlines(40)
print s
ser.close()



if __name__ == '__main__':
    all_set()

'''