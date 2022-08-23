from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException,ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest

import json,os,re,time
from os import popen
from os.path import exists,join,dirname

IP_FILE_PATH = join(dirname(__file__),'ipali.txt')
def gen_ip_file(ip_addr):
    with open(IP_FILE_PATH,'w',encoding="utf-8") as f:
        f.write(ip_addr)
def get_ip_file_content():
    with open(IP_FILE_PATH,'r',encoding="utf-8") as f:
        return f.read()

#client = AcsClient('ID', 'KEY', 'cn-hangzhou')

def get_internet_ip():
    cmd = 'curl http://httpbin.org/ip -s silent'
    cmd_pipe = popen(cmd)
    cmd_ret = ''.join(cmd_pipe.readlines())
    regex = r'(\d+\.){3}\d+'
    return str(re.search(regex, cmd_ret).group(0))

#ip = get_internet_ip()
#print(get_internet_ip())

def Describe_SubDomain_Records(client,record_type,subdomain):
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_Type(record_type)
    request.set_SubDomain(subdomain)
    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult

#以下是函数调用以及说明
#des_relsult = Describe_SubDomain_Records(client,"A","domain_name")
#print(des_relsult["TotalCount"])#：解析记录的数量，0表示解析记录不存在，1表示有一条解析记录
#print(des_relsult["DomainRecords"]["Record"][0]["RecordId"]) #：当des_relsult["TotalCount"]为1时，会返回这个RecordId，后续的修改域名解析记录中需要用到
#print(des_relsult["DomainRecords"]["Record"][0]["Value"])

def add_record(client,priority,ttl,record_type,value,rr,domainname,line):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_DomainName(domainname)
    request.set_Line(line)
    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult

#函数调用
#add_relsult = add_record(client,"5","600","A",ip,"sz","huangwx.cn")
#record_id = add_relsult["RecordId"]#同样会返回一个RecordId，修改的时候也可以直接调用

def update_record(client,priority,ttl,record_type,value,rr,record_id,line):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_RecordId(record_id)
    request.set_Line(line)
    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    return response

#函数调用
#record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
#rr=update_record(client,"5","600","A",'1.83.48.234',"out",record_id,"telecom")
#print(rr)

def update_ip(ip_addr:str):
    try:
        client = AcsClient('ID', 'KEY', 'cn-hangzhou')
    except:
        print('Client connection failed!')
        return False
    subdomain="subdomain_name"
    domainname='domain_name'
    des_relsult = Describe_SubDomain_Records(client,"A",subdomain+'.'+domainname)
    if des_relsult["TotalCount"] == 0:
        add_relsult = add_record(client,"5","600","A",ip_addr,subdomain,domainname,"telecom")
        print("The domainname is added. Please try it 1 minute later!")
        status=True
    #判断子域名解析记录查询结果，TotalCount为1表示存在这个子域名的解析记录，需要更新解析记录，更新记录需要用到RecordId，这个在查询函数中有返回des_relsult["DomainRecords"]["Record"][0]["RecordId"]
    elif des_relsult["TotalCount"] == 1:
        if des_relsult["DomainRecords"]["Record"][0]["Value"]!=ip_addr:
            record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
            update_record(client,"5","600","A",ip_addr,subdomain,record_id,"telecom")
            print("The ip address is updated. Please try it 1 minute later!")
        else:
            print("The ip address is not changed. Please use it.")
        status=True
    else:
        print("There exist duplicate domain names. Please check it!")
        status=False
    return status

if __name__ == '__main__':
    native_ip = get_internet_ip()
    if "" == native_ip:
        print("Falied in acquiring the ip address.")
        quit(-1)
    if not exists(IP_FILE_PATH):
        if update_ip(native_ip):
            gen_ip_file(native_ip)
    else:
        if get_ip_file_content().strip() == native_ip:
            print("The ip address is not changed. Please use it.")
        else:
            if update_ip(native_ip):
                gen_ip_file(native_ip)