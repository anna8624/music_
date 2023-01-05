"""
Auther:Anna
File Name:DownloadThread.py
建立時間:2022/11/22,下午 08:21
TODO:
"""
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.support.wait import WebDriverWait


class DownloadThread(QThread):
    callback=pyqtSignal(object)
    finished=pyqtSignal()
    def __init__(self, browser, chks, path):
        super().__init__(None)
        self.browser=browser
        self.chks=chks
        self.path=path
    def run(self):
        files=os.listdir(self.path)
        for file in files:
            if '.crdownload' in file:
                path=os.path.join(self.path, file)
                os.remove(path)
        for i, chk in enumerate(self.chks):
            title=chk.split(' url=')[0]
            url=chk.split(' url=')[1].replace('youtube', 'backupmp3')
            self.callback.emit(f'正在下載 {title}....')
            self.browser.get(url)
            self.browser.switch_to.frame('IframeChooseDefault')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'MP3Format')))
                btn=self.browser.find_element(By.ID,'MP3Format')
                btn.click()
                self.sleep(3)
            except:
                pass
            try:
                WebDriverWait(self.browser,200,1).until(self.download_finished)
            except:
                print(f'{title}無法下載')

        self.finished.emit()
    def download_finished(self, browser):
        files=os.listdir(self.path)
        finished=True
        for file in files:
            if ".crdownload" in file:
                finished=False
                break
        return finished