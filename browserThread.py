"""
Auther:Anna
File Name:browserThread.py
建立時間:2022/11/17,下午 08:55
TODO:
"""
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserThread(QThread):
    callback=pyqtSignal(object) #產生一支電話，打給ui主執行續用的
    def __init__(self,path):
        super().__init__(None)
        self.browser=None
        self.path=path
    def run(self):  #要執行的任務都放在run方法裡面
        opt=Options()
        opt.add_argument('--headless')  #無頭模式，沒有視窗
        opt.add_argument('disable-gpu')
        opt.add_experimental_option('detach', True) #註解後，瀏覽器會自動關閉
        opt.add_experimental_option('excludeSwitches',['enable-lodding']) #允許chrome可以下載
        #更改預設下載目錄
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.path}
        opt.add_experimental_option('prefs', prefs)
        service=Service(ChromeDriverManager().install())
        browser=webdriver.Chrome(service=service,options=opt)
        self.callback.emit(browser)  #發射，打電話回ui主執行序

