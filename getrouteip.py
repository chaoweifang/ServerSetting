from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.webdriver.support.ui as ui
import time
import os
from datetime import datetime

def get_ip(browser=None):
    options = Options()
    options.add_argument('--headless')
    # 打开浏览器
    browser = webdriver.Firefox(options=options)
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

if __name__ == "__main__":
    #ReadRouterIP()
    print(get_ip())

