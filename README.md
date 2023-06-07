## 注意事项
重装时切勿对/home和/data的专有分区（重装前通过指令“df -hl”查看）进行格式化和挂载，重装系统后修改/etc/fstab实现对home和data专有分区的挂载！

## 服务器验收
1. 检查显卡：
    - `lspci | grep -i nvidia`
    - `nvidia-smi`
2. 检查cpu: `cat /proc/cpuinfo`
3. 检查内存： `free -m`
4. 检查磁盘：
    - `sudo lsblk`
    - `sudo fdisk -l`
5. 查看分区挂载情况：`df -hl`

## 服务器配置
1. 挂载磁盘： 重装时切勿对/home或者/data的专有分区（重装前通过指令`df -hl`查看）进行格式化和挂载，重装系统后修改/etc/fstab实现对home和data专有分区的挂载，即添加：
    + UUID=xxxx /home           ext4    defaults        0       2
    + UUID=xxxx /data           ext4    defaults        0       2
2. 添加端口转发规则
3. 内网穿透配置： 见“autossh-readme.md”
4. 动态域名设置: 见“dynamic-domain-readme.md”
5. 修改hostname
    + `sudo hostname xxx`
    + `sudo vim /etc/hosts`
    + 添加内容： 127.0.0.1 xxx
6. dns修改
    + `sudo vim /etc/resolv.conf`
    + 添加：
        - nameserver 114.114.114.114
        - nameserver 8.8.8.8
    + 永久停止 ubuntu 默认 DNS 本地服务:
        `sudo systemctl disable --now systemd-resolved`
    + 修改 NetworkManager：
        - 打开文件: `sudo vim /etc/NetworkManager/NetworkManager.conf`
        - 在[main] 节点下增加下面的配置： dns=none
        - 重启 NetworkManager： `sudo systemctl restart NetworkManager`
        - 按照暂时修改的方法进行配置即可, 重启电脑或网络不会覆盖`resolv.conf`
7. 修改密码，创建账号
    + 修改密码：`sudo password xxx`
    + 添加账号：`sudo adduser [用户名]`
    + 若需添加超级权限则执行：`sudo usermod -aG sudo [用户名]`
    + 重装系统时候，若home中已存在新添加账号的目录，需对其归属权进行修改：`sudo chown -R [用户名]:[用户名] [用户名]`
    + 添加密钥：见[服务器密钥登录教程](https://docs.qq.com/doc/DTVdTTUJNcWtvTWJp)
8. 显卡驱动安装
    + 选择合适的版本，下载[驱动文件](https://www.nvidia.com/download/index.aspx?lang=en-us)
    + 执行以下指令进行安装：
        - `sudo service lightdm stop` //关闭图形界面
        - `sudo chmod a+x NVIDIA-Linux-x86_64-396.18.run`
        - `sudo ./NVIDIA-Linux-x86_64-396.18.run -no-x-check -no-nouveau-check -no-opengl-files` //禁用opengl, 防止出现循环登陆现象
        - 安装过程中出现yes或者no选项，默认即可
9. CUDA安装
    + 选择合适的版本，下载[runfile文件](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu)
    + 执行以下指令进行安装：
        - `chmod +x cuda文件名`
        - `sudo ./cuda文件名`
    + 重启，nvidia-smi查看显卡是否正常
10. 时区设置：`sudo timedatectl set-timezone Asia/ShangHai`
11. 禁用账号密码远程登陆并keep alive
    + 修改/etc/ssh/sshd_config： PasswordAuthentication no; TCPKeepAlive yes; ClientAliveInterval 0; ClientAliveCountMax 3
    + 重启sshd服务： `sudo service sshd restart`
    + 检查ssh连接能否正常登录服务器
12. 分配swap空间
    + `free -m`
    + `sudo swapoff -a`
    + `free -m`
    + `sudo fallocate -l 64GB /swapfile`
    + `sudo chmod 600 /swapfile`
    + `sudo mkswap /swapfile`
    + `sudo swapon /swapfile`
    + `free -h`
    + 然后编辑/etc/fstab, 在末尾添加： /swapfile none swap sw 0 0
    + `free -m`
13. 禁止自动休眠：
    + `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`
14. 常用软件和代码库安装：
    + `sudo apt install xfce4`
    + `sudo apt install autossh`
    + x2goserver:
        - `sudo apt-get install software-properties-common`
        - `sudo add-apt-repository ppa:x2go/stable`
        - `sudo apt-get update`
        - `sudo apt-get install x2goserver x2goserver-xsession`
    + [Anaconda](https://www.anaconda.com/download#downloads):
        - `wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh`
        - `chmod +x ./Anaconda3-2023.03-1-Linux-x86_64.sh`
        - `sudo ./xxx.sh`
    + `sudo apt install tmux`
    + `sudo apt install git`
    + `sudo apt install vim`
    + `sudo apt instal python-pip3`
    + [PyTorch](https://pytorch.org/get-started/locally/):
        - `sudo pip install opencv-contrib-python`
        - `sudo pip install selenium`
    + [Geckodriver](https://github.com/mozilla/geckodriver/releases):
        - 下载并解压
        - `cp geckodriver /usr/bin`
15. pip 换源：
    + `vim ~/.pip/pip.conf`
    + 添加以下内容：
    ```
    [global]
    index-url=https://pypi.tuna.tsinghua.edu.cn/simple
    [install]
    trusted-host=mirrors.aliyun.com
    ```
16. conda换源：

    + 展示已有源链接： `conda config --show-sources`
    + `vim .condarc`
    + 添加各种镜像源：
    ```
    channels:
      - defaults
    show_channel_urls: true
    channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
    default_channels:
      - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
      - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
      - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
      - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
      - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
    custom_channels:
      conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
      msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
      bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
      menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
      pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
      simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
    ```

17. apt install 换源:
    + 获取ubuntu版本号： `lsb_release -a`
    + cd /etc/apt/
    + 备份原sources文件： `sudo cp sources.list sources.list_bak`
    + 根据ubuntu版本号修改sources文件，例如ubuntu版本号为jammy，则可：
        - `sudo vim sources.list`
        - 添加以下内容：
            ```
            deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
            deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
            deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
            deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
            deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
            deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
            deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
            deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
            deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
            deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
            ```
        - `sudo apt update`

18. 常用指令：
    + 文件查看
        - 查看当前目录下一级文件夹大小： `sudo ls | xargs sudo du -ksh`
        - 查看当前目录占用的总磁盘大小： `sudo du -sh`
    + 端口
        - 端口占用情况：`sudo netstat -ap | grep port`
        - 查看占用端口的PID: `sudo lsof -i :7002`
    + 休眠
        - 禁用： `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`
        - 恢复： `sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target`
