#/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
from os import popen,getcwd
from os.path import exists,join,dirname
import re

IP_FILE_PATH = join(dirname(__file__),'ip.txt')

def gen_ip_file(ip_addr):
    with open(IP_FILE_PATH,'w',encoding="utf-8") as f:
        f.write(ip_addr)
def get_ip_file_content():
    with open(IP_FILE_PATH,'r',encoding="utf-8") as f:
        return f.read()


def get_native_ip():
    cmd = 'ifconfig | grep "inet .*10\." | head -1'
    cmd_pipe = popen(cmd)
    cmd_ret = cmd_pipe.readline()
    regex = r'(\d+\.){3}\d+'
    return str(re.search(regex, cmd_ret).group(0))


def update_ip(ip_addr:str):
    hostname="host_name"
    url = "http://members.3322.net/dyndns/update"
    params = {
        'system':'dyndns',
        'hostname':hostname,
        'myip':ip_addr
    }
    response = requests.get(url=url, params=params, auth=('username','password'))

    if response.text.startswith('good') or response.text.startswith('nochg'):
        return True
    else:
        return False

if __name__ == '__main__':
    native_ip = get_native_ip()
    if "" == native_ip:
        print("ip di zhi huo qu wei cheng gong")
        quit(-1)
    if not exists(IP_FILE_PATH):
        if update_ip(native_ip):
            print("jie xi cheng gong,qing yi feng zhong zhi hou shi")
            gen_ip_file(native_ip)
        else:
            print("jie xi shi bai")
    else:
        if get_ip_file_content().strip() == native_ip:
            print("ip mei bian, ke yi shi yon")
        else:
            #print('ok',native_ip)
            if update_ip(native_ip):
                print("jie xi cheng gong ")
                gen_ip_file(native_ip)
            else:
                print("jie xi shi bai")
