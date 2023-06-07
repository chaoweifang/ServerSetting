
## 基本规则

| 名称     | 解释 |
| ---     | --- |
| 服务器A  | 需要内网穿透的机器 |
| 中转机   | 具有公网IP的中转机器 |
| 转发端口 | 最好设置为8000以上的端口 |

本教程将介绍如何利用中转机实现对服务器A的外网访问

## 登陆服务器

`ssh [服务器A用户名]@[中转机IP] -p [转发端口]`

## 流程
1. 登录中转机,如阿里云轻量应用服务器, 开放对应**转发端口**的防火墙
    - 阿里云轻量应用服务器参考网页 : [防火墙](https://help.aliyun.com/document_detail/59086.html)
    - 或者进入中转机：
        + 打开转发端口的防火墙：
            - 方式1
        
                `sudo firewall-cmd --zone=public --add-port=转发端口/tcp --permanent`

                `sudo firewall-cmd --reload`

            - 方式2
        
                `sudo ufw enable`

                `sudo ufw allow 转发端口/tcp`

                `sudo ufw reload`

        + 设置GatewayPorts yes: 
    
            ` sudo vim /etc/ssh/sshd_config`

            ` 修改： GatewayPorts yes`

            ` sudo service sshd restart`

2. 在服务器A的linux上安装autossh： 
    `sudo apt install autossh`

3. 服务器A**免密登陆**到中转机，在服务器A上执行如下命令：

    `ssh-keygen -t rsa`

4. 如果可以使用ssh从服务器A连接中转机，则执行：`ssh-copy-id [中转机username]@[中转机IP]`； 否则，联系管理员手动添加公钥。
    
5. 在服务器A上输入如下指令, 
    - 测试autossh:
        `autossh -p sshport -M 监听端口 -NR '*:转发端口:127.0.0.1:22' [中转机username]@[中转机IP]`
    - 在**中转机**上测试对应端口是否处于监听状态: 
        `netstat -tupln`
    - 结束在服务器A上的autossh命令
   
6. 在**服务器A**上编写守护进程, 使得服务器A在开机联网以后能够自动autossh
    - 参考网页 : [为 autoSSH 端口转发配置 systemd 守护进程](https://roriri.one/2019/01/19/autossh/)
    - 守护进程模板，见"autossh-nwct.service":
    
    ```bash
    [Unit]
    Description=AutoSSH tunnel service
    Wants=network-online.target
    After=network.target network-online.target ssh.service
    
    [Service]
    Environment="AUTOSSH_GATETIME=0"
    User=[服务器A用户名]
    ExecStart=/usr/bin/autossh -p sshport -M 监听端口 -NR '*:转发端口:127.0.0.1:22' [中转机username]@[中转机IP]
    
    ExecStop=/usr/bin/killall -s KILL autossh
    
    [Install]
    WantedBy=multi-user.target
    ```

    - 它会在系统启动并且网络连通了、sshd服务也加载完了之后就启动 autossh服务。需要把这个文件放在 **/etc/systemd/system** 内，文件名以 **.service** 结尾

        + 刷新systemd守护进程列表:
            `sudo systemctl daemon-reload`
        + 启动服务:
            `sudo service [YOUR SERVICE FILE NAME] start`
        + 查看服务:
            `service [YOUR SERVICE FILE NAME] status`
        + 如果您看到了类似以下的字符串：

            > Active: active (running) since Fri 2018-02-23 22:28:49 UTC; 7s ago

            那么说明服务启动成功了，否则请重新检查配置。

        + 最后，设置服务开机自动启动：  
            `sudo systemctl enable [YOUR SERVICE FILE NAME]`

## 最后遇事不决,一键重启,或者自行百度谷歌


<!-- <meta http-equiv="refresh" content="1"> -->