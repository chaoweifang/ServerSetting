## 原理
1. 使用python http请求库动态更新ip到动态域名免费供应商pubyun.com账户或阿里云付费账户
2. 每次当ip变化时候就会触发更新
3. 使用crontab定时任务监控该任务

## Prerequisite
系统自带的python3或者制定python3环境装以下包
```bash
pip3 install aliyun-python-sdk-core-v3
pip3 install aliyun-python-sdk-domain
pip3 install aliyun-python-sdk-alidns
pip3 install selenium
pip3 install requests
```
以上命令视情况而定，目前仅在python3中测试通过，没有在python2中进行测试

下载`geckodriver`: https://github.com/mozilla/geckodriver/releases, 解压并将`geckodriver`复制至`/usr/local/bin/`目录中：
+ sudo cp geckodriver /usr/local/bin/
+ sudo chmod +x /usr/local/bin/geckodriver

## 申请域名信息（以pubyun为例）
1. 进入 http://www.pubyun.com/ 注册账号信息，登录
2. 申请域名
      + 进入动态域名->创建域名
      + 选择免费版，点击创建动态域名

## 修改定期映射代码
1. 修改`update_parse_domain_xxx.py`文件中的账号信息
      + update_parse_domain_aliyun_global.py: 适用于拥有公网ip的服务器，需从阿里云获取ID、Key、subdomain_name、domain_name信息，并替换相应的变量；
      + update_parse_domain_pubyun_global.py: 适用于拥有公网ip的服务器，需从pubyun获取username、password、hostname信息，并替换相应的变量；
      + update_parse_domain_pubyun_local.py： 服务器挂在拥有校园局部网ip的路由器下时，可使用该代码，需从pubyun获取username、password、hostname信息，并替换相应的变量；
      
2. 修改`update_parse_domain.sh`文件信息
```sh
# 下面的python路径和py文件修改为实际的绝对路径
/usr/bin/python3 /home/tools/update_parse_domain_xxx.py > /home/tools/cron002.txt 2>&1 &
```
需保证'/home/tools/'目录可读写

3. 添加定时任务
```bash
crontab -e
```
上述命令打开后(如果没有安装 crontab自行百度如何安装)，在新开的vim或者nano界面中添加一行，表示每隔5分钟执行上面sh脚本一次
```bash
# 这三行如果之前没有请务必添加
PATH=/sbin:/bin:/usr/sbin:/usr/bin
SHELL=/bin/bash
MAILTO=""

# 添加改行 ~/tools/update_domain_parse.sh这里改为上面sh文件的路径
*/5 * * * * /home/tools/update_parse_domain.sh
```

<meta http-equiv="refresh" content="2">

