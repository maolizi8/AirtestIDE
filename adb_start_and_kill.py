'''
Created on 2019年8月1日

@author: geqiuli
'''
import subprocess
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('BASE_DIR :',BASE_DIR)

def init_AirtestIDE_adb(device=None, port='5037'):
    '''启动adb，device为设备号'''
    adb_path=os.path.join(BASE_DIR,'airtest','core','android','static','adb','windows','adb.exe')
    print('adb_path :',adb_path)
    if device:
        cmd_str=adb_path +' -P ' + port +' -s '+device
    else:
        cmd_str=adb_path +' -P ' + port
    print('command: ',cmd_str)
    subprocess.run(cmd_str)
    #subprocess.run(cmd_str, shell=True, check=True)

def kill_AirtestIDE_adb(port='5037'):
    '''关闭adb'''
    adb_path=os.path.join(BASE_DIR,'airtest','core','android','static','adb','windows','adb.exe')
    print('adb_path :',adb_path)
    cmd_str=adb_path +' -P ' + port + ' kill-server'
    print('command: ',cmd_str)
    subprocess.run(cmd_str)
    #subprocess.run(cmd_str, shell=True, check=True)     
    
if __name__ == '__main__':
    kill_AirtestIDE_adb()
    #init_AirtestIDE_adb('02157df271610a1b')
