"""
Auther:Anna
File Name:SearchThread.py
建立時間:2022/11/22,下午 06:43
TODO:
"""
from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SearchThread(QThread):
    callback=pyqtSignal(object)
    def __init__(self,browser,song):
        super().__init__(None)
        self.browser=browser
        self.song=song
    def run(self):
        self.browser.get(f'https://www.youtube.com/results?search_query={self.song}')
        links={}
        try:
            WebDriverWait(self.browser, 20,5).until(EC.presence_of_element_located((By.ID,'video-title')))
            tags=self.browser.find_elements(By.TAG_NAME,'a')
            for tag in tags:
                href=tag.get_attribute('href')
                if 'watch' in str(href):
                    title=tag.get_attribute('title')
                    if title=="":
                        try:
                            title=tag.find_element(By.ID,'video-title').get_attribute('title')
                        except:
                            pass
                    if title!="":
                        links[href]=f'{title} url={href}'
        except Exception as e:
            print(e)
        # print(links)
        self.callback.emit(links)
