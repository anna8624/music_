"""
Auther:Anna
File Name:mp3.py
建立時間:2022/11/17,下午 08:25
TODO:
"""
# 啟動錯誤訊息 log : run/Edit configuration/Emulate terminal in output console

import os.path
import sys

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListWidgetItem, QFileDialog

from DownloadThread import DownloadThread
from SearchThread import SearchThread
from browserThread import BrowserThread
from ui.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self) #繪製qtdesigner所設計出來的ui
        self.resize(1200,800)
        self.path="d:\\mp3_tmp"  #一定要用"\\"
        self.lblPath.setText(self.path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.disabledGui()
        self.browserTread=BrowserThread(self.path) #聘請新員工
        self.browserTread.callback.connect(self.browserTreadCallback) #callback打電話給老闆
        self.browserTread.start() #叫這個新員工開始工作
        self.btnSearch.clicked.connect(self.btnSearch_click)
        self.btnDownload.clicked.connect(self.btnDownload_click)
        self.btnPath.clicked.connect(self.btnPath_click)

        #按下Enter就開始查詢
        self.txtSong.installEventFilter(self)

    def btnPath_click(self):
        path = QFileDialog.getExistingDirectory()
        if path != '':
            self.path = path.replace("/", "\\")
            self.lblPath.setText(self.path)
            self.disabledGui()
            # self.browser.close()
            self.browser.quit()
            self.browserThread = BrowserThread(self.path)
            self.browserThread.callback.connect(self.browserThreadCallback)
            self.browserThread.start()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and source is self.txtSong):
            if event.text() == "\r":
                self.btnSearch_click()
        return super(MainWindow, self).eventFilter(source, event)

    def btnDownload_click(self):
        count = self.listWidget.count()
        boxes = [self.listWidget.itemWidget(self.listWidget.item(i)) for i in range(count)]
        chks = []
        for box in boxes:
            if box.isChecked():
                chks.append(box.text())
        self.disabledGui()
        self.downloadThread = DownloadThread(self.browser, chks, self.path)
        self.downloadThread.callback.connect(self.downloadThreadCallback)  # 第一支電話
        self.downloadThread.finished.connect(self.downloadThreadFinished)  # 第二支電話
        self.downloadThread.start()

    def downloadThreadCallback(self, msg):
        self.lblStatus.setText(msg)

    def downloadThreadFinished(self):
        self.lblStatus.setText('下載完成')
        self.enabledGui()

    def btnSearch_click(self):
        self.listWidget.clear()
        self.song=self.txtSong.text()
        if self.song=='':
            dialong=QMessageBox()
            dialong.setWindowTitle("mp3")
            dialong.setText("請輸入歌手/歌曲")
            dialong.exec()
            return
        self.lblStatus.setText("搜尋中...")
        self.searchThread=SearchThread(self.browser,self.song) #找一個新員工來查詢
        self.searchThread.callback.connect(self.searchThreadCallBack)
        self.searchThread.start()

    def searchThreadCallBack(self,links):
        self.enabledGui()
        self.lblStatus.setText('')
        for key in links.keys():
            item=QListWidgetItem()
            self.listWidget.addItem(item)
            box = QCheckBox(links[key])
            self.listWidget.setItemWidget(item,box)

    def browserTreadCallback(self,browser):
        self.browser=browser
        self.enabledGui()

    def disabledGui(self):
        self.txtSong.setEnabled(False)
        self.btnPath.setEnabled(False)
        self.btnDownload.setEnabled(False)
        self.btnSearch.setEnabled(False)
    def enabledGui(self):
        self.txtSong.setEnabled(True)
        self.btnPath.setEnabled(True)
        self.btnDownload.setEnabled(True)
        self.btnSearch.setEnabled(True)

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    app.exec() #等待迴圈，監控滑鼠鍵盤，更新視窗