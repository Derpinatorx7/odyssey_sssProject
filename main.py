import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

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
        self.mainView = QtWidgets.QFrame()
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.initButton("upload",70,10, self.hideCurrentView,BUTTONSTYLESHEET), 1, 0)
        mainLayout.addWidget(self.initButton("download",10,70, self.hideCurrentView,BUTTONSTYLESHEET), 1, 1)
        mainLayout.addWidget(self.initButton("master download",40,100, self.hideCurrentView,BUTTONSTYLESHEET), 1, 2)
        self.mainView.setLayout(mainLayout)
        
        self.mainView.setParent(self)


    def initUploadView(self):
        pass

    def initDownloadView(self):
        pass

    def initMasterDownloadView(self):
        pass
 
    def hideCurrentView(self):
        if self.currentView == "main":
            self.mainView.hide()
    
    def showUploadView(self):
        self.hideCurrentView()
        self.currentView = "upload"
        self.uploadView.show()
    
    def showDownloadView(self):
        self.hideCurrentView()
        self.currentView = "download"
        self.downloadView.show()
    
    def showMasterDownloadView(self):
        self.hideCurrentView()
        self.currentView = "master download"
        self.masterDownloadView.show()

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