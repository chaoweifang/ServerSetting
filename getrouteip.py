from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
import time
import os
from datetime import datetime
from os import popen,getcwd
import re

# huo qu ben ji ip di zhi
def get_native_ip():
    cmd = 'ifconfig | grep "inet .*10\." | head -1'
    cmd_pipe = popen(cmd)
    cmd_ret = cmd_pipe.readline()
    regex = r'(\d+\.){3}\d+'
    return str(re.search(regex, cmd_ret).group(0))

# get ip from internet. you gong wang ip ke yi shi yong. 
def get_internet_ip():
    cmd = 'curl http://httpbin.org/ip -s silent'
    cmd_pipe = popen(cmd)
    cmd_ret = ''.join(cmd_pipe.readlines())
    regex = r'(\d+\.){3}\d+'
    return str(re.search(regex, cmd_ret).group(0))

# get router wan ip: TP-LINK TL-R473G
def get_ip_tl_r473g(browser=None):
    options = Options()
    options.add_argument('--headless')
    # 打开浏览器
    #browser = webdriver.Firefox(options=options)
    browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", service_log_path=os.path.join(os.path.dirname(__file__),'geckodriver.log'), options=options)
    assert browser
    try:
        # 打开路由器登录网页
        browser.get("http://tplogin.cn/")
        # 设置等待时间
        wait = ui.WebDriverWait(browser, 5)
        # ---- 用户登录 ---- #
        # 等待登录页面加载完毕
        wait.until(lambda driver: driver.find_element_by_id('login-btn'))
        # 输入密码
        js = "document.getElementById('username').value='username'"
        browser.execute_script(js)
        js = "document.getElementsByClassName('text-text password-text password-hidden login')[0].value='password'"
        browser.execute_script(js)
        js = "document.getElementById('login-btn').click()"
        browser.execute_script(js)
        # 点击登录
        #browser.find_element_by_id('login-btn').click()
        #print('login succeed')
        # ---- 界面查找 ---- #
        # 等待路由器设置界面加载完毕
        time.sleep(5)
        #file_object=open('test.html','w')
        #file_object.write(browser.page_source)
        #file_object.close()
        wait.until(lambda driver: driver.find_element_by_id('wan'))
        wan = browser.find_element_by_id('wan')
        ip = wan.find_elements_by_class_name('ipaddr')[0]
        ip_string=ip.text
        browser.close()
        browser.quit()
        return ip_string
    except:
        browser.close()
        browser.quit()
        return None

# get router wan ip: TP-LINK TL-R479G+
# need to specify username and password
def get_ip_tl_r479g(browser=None):
    options = Options()
    options.add_argument('--headless')
    # 打开浏览器
    #print(os.path.join(os.path.dirname(__file__),'geckodriver.log'))
    browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", service_log_path=os.path.join(os.path.dirname(__file__),'geckodriver.log'), options=options)
    assert browser
    try:
        # 打开路由器登录网页
        browser.get("http://tplogin.cn/")
        #print(0)
        # 设置等待时间
        wait = ui.WebDriverWait(browser, 5)
        #print('0-1')
        # ---- 用户登录 ---- #
        # 等待登录页面加载完毕
        wait.until(lambda driver: driver.find_element('id','login-btn'))
        #print(1)
        # 输入密码
        js = "document.getElementById('username').value='username'"
        browser.execute_script(js)
        #print(2)
        js = "document.getElementsByClassName('text-text password-text password-hidden login')[0].value='password'"
        browser.execute_script(js)
        #print(3)
        js = "document.getElementById('login-btn').click()"
        browser.execute_script(js)
        #print(4)
        # 点击登录
        #browser.find_element_by_id('login-btn').click()
        #print('login succeed')
        # ---- 界面查找 ---- #
        # 等待路由器设置界面加载完毕
        time.sleep(5)
        wait.until(lambda driver: driver.find_element('id','menu-advanced-running-status-li'))
        rs=browser.find_element('name','running-status')
        action = ActionChains(browser)
        action.move_to_element(rs).click().perform()
        #js = "document.getElementsByClassName('running-status')[0].click()"
        #browser.execute_script(js)
        #print('click router go wan')
        time.sleep(15)
        #等待路由器加载WAN信息
        wait.until(lambda driver: driver.find_element('id','wan1'))
        #file_object=open('test.html','w')
        #file_object.write(browser.page_source)
        #file_object.close()
        wan = browser.find_element('id','wan1')
        ip = wan.find_elements('class name','ipaddr')[0]
        #print('ip:', ip.get_attribute('textContent'))
        ip_string=ip.get_attribute('textContent')
        browser.close()
        browser.quit()
        return ip_string
    except:
        browser.close()
        browser.quit()
        return None

if __name__ == "__main__":
    #ReadRouterIP()
    print(get_ip())

