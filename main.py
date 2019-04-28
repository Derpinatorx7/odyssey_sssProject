import sys
import socket
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from user import packOpenReq

BUFFER = 4096

BUTTONSTYLESHEET = '''QPushButton {background-color: red;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px;}
    QPushButton:pressed {
    background-color: rgb(224, 0, 0);
    border-style: inset;}'''

LABELSTYLESHEET = '''border: 10px solid;
border-color: rgb(224, 0, 0);
border-radius: 20px;
font: bold 8pt "Open Sans";
text-align: center;
color: rgb(224, 0, 0);
background-color: rgb(255, 255, 255);
'''

LINEEDITSTYLESHEET = '''border: 10px solid;
    border-color: rgb(255, 255, 255);
    border-radius: 20px;
    font: bold 8pt "Open Sans";
    text-align: center;
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);'''
##########
# Consts #
##########
OG_BACKGROUND_FILE = "background.png"
DOWNLOAD_BACKGROUND_FILE = "background.png"
UPLOAD_BACKGROUND_FILE = "background.png"

class App(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.currentView = "main"
        self.downloadEdits = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.initMainView()
        self.initUploadView()
        self.initDownloadView()
        self.initMasterDownloadView()
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setBackground(OG_BACKGROUND_FILE)

        self.show()
        
    def setBackground(self,background):
        oImage = QtGui.QImage(background)
        sImage = oImage.scaled(QtCore.QSize(self.width,self.height))                   # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)


    def initMainView(self):
        global BUTTONSTYLESHEET
        self.mainView = QtWidgets.QFrame()
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addItem(QtWidgets.QSpacerItem(40, 400),0,0)
        mainLayout.addWidget(self.initButton("upload",70,10, self.showUploadView,BUTTONSTYLESHEET), 1, 0)
        mainLayout.addWidget(self.initButton("download",10,70, self.showDownloadView,BUTTONSTYLESHEET), 1, 1)
        mainLayout.addWidget(self.initButton("master download",40,100, self.showMasterDownloadView,BUTTONSTYLESHEET), 1, 2)
        self.mainView.setLayout(mainLayout)
        self.mainView.setParent(self)




    def initUploadView(self):
        pass


    def initDownloadView(self):
        global LABELSTYLESHEET, LINEEDITSTYLESHEET, BUTTONSTYLESHEET
        self.downloadView = QtWidgets.QFrame()
        downloadLayout = QtWidgets.QGridLayout()
        downloadLayout.addItem(QtWidgets.QSpacerItem(10,50),0,0)
        nameLabel = QtWidgets.QLabel("downloadLabel")
        nameLabel.setText("Enter arcname")
        nameLabel.setStyleSheet(LABELSTYLESHEET)
        downloadLayout.addWidget(nameLabel,1,1)
        nameEdit = QtWidgets.QLineEdit("archive name")
        nameEdit.setText("archive name")
        nameEdit.setStyleSheet(LINEEDITSTYLESHEET)
        
        self.downloadEdits["nameEdit"] = nameEdit
        downloadLayout.addWidget(nameEdit, 1, 2)
        downloadLayout.addItem(QtWidgets.QSpacerItem(0, 100),2,1)
        downloadLabel = QtWidgets.QLabel("downloadLabel")
        downloadLabel.setText("Enter Email")
        downloadLabel.setStyleSheet(LABELSTYLESHEET)
        downloadLayout.addWidget(downloadLabel,3,1)

        emailEdit = QtWidgets.QLineEdit("email")
        emailEdit.setText("enter your mail")
        emailEdit.setStyleSheet(LINEEDITSTYLESHEET)
        self.downloadEdits["emailEdit"] = emailEdit
        downloadLayout.addWidget(emailEdit, 3, 2)
        downloadLayout.addItem(QtWidgets.QSpacerItem(0, 100),4,1)

        xEdit = QtWidgets.QLineEdit("Enter password x coordinate")
        xEdit.setText("x coordinate")
        xEdit.setStyleSheet(LINEEDITSTYLESHEET)
        yEdit = QtWidgets.QLineEdit("Enter password y coordinate")
        yEdit.setText("y coordinate")
        yEdit.setStyleSheet(LINEEDITSTYLESHEET)
        self.downloadEdits["xEdit"] = xEdit
        downloadLayout.addWidget(xEdit, 5, 1)
        self.downloadEdits["yEdit"] = yEdit
        downloadLayout.addWidget(yEdit, 5, 3)

        passwordLabel = QtWidgets.QLabel("passwordLabel")
        passwordLabel.setText("enter x and y coordinates")
        passwordLabel.setStyleSheet(LABELSTYLESHEET)
        self.downloadEdits["passwordLabel"] = passwordLabel
        downloadLayout.addWidget(passwordLabel,5,2)
        downloadLayout.addWidget(self.initButton("submitButton",0,0,self.sendOpenReq,BUTTONSTYLESHEET),6,3)
        
        self.downloadView.setLayout(downloadLayout)

    def sendOpenReq(self):
        global BUFFER
        msg = packOpenReq(self.downloadEdits["nameEdit"].text(),self.downloadEdits["emailEdit"].text(),(int(self.downloadEdits["xEdit"].text()),int(self.downloadEdits["yEdit"].text())))
        
        s = socket.socket()
        s.connect(("127.0.0.1",8087))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

    def initMasterDownloadView(self):
        pass
 
    def hideCurrentView(self):
        if self.currentView == "main":
            self.mainView.setParent(None)
            self.mainView.hide()
        if self.currentView == "upload":
            self.uploadView.setParent(None)
            self.uploadView.hide()
        if self.currentView == "download":
            self.downloadView.setParent(None)
            self.downloadView.hide()
        if self.currentView == "master download":
            self.masterDownloadView.setParent(None)
            self.masterDownloadView.hide()

    def showUploadView(self):
        self.hideCurrentView()
        self.currentView = "upload"
        self.uploadView.setParent(self)
        self.uploadView.show()
    
    def showDownloadView(self):
        self.hideCurrentView()
        self.currentView = "download"
        self.downloadView.setParent(self)
        self.downloadView.show()

    def showMasterDownloadView(self):
        self.hideCurrentView()
        self.currentView = "master download"
        self.masterDownloadView.setParent(self)
        self.masterDownloadView.show()

    def showMainView(self):
        self.hideCurrentView()
        self.currentView = "main"
        self.mainView.show()

    def initButton(self, buttonName, x, y, method, styleSheet) :
        button = QtWidgets.QPushButton(buttonName, self)
        button.setToolTip('es el caftoro {}'.format(buttonName))
        button.move(x,y)
        button.clicked.connect(method)
        button.setStyleSheet(styleSheet)
        return button

    def onClick(self):
        print('lol gadol')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())