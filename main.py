import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui

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
        self.currentWindow = "main"
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.initMainView()
        self.initUploadView()
        self.initDownloadView()
        self.initMasterDownloadView()
        
        self.setLayout(self.mainView)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.show()
        
    def setBackground(self,background):
        bg = QtGui.QImage(background)
        self.layout.addWidget(bg)

    def initMainView(self):
        self.mainView = QtWidgets.QGridLayout()
        self.mainView.addWidget(self.initButton("upload",70,10, self.on_click), 1, 0)
        self.mainView.addWidget(self.initButton("download",10,70, self.on_click), 1, 1)
        self.mainView.addWidget(self.initButton("master download",40,100, self.on_click), 1, 2)

    def initUploadView(self):
        pass

    def initDownloadView(self):
        pass

    def initMasterDownloadView(self):
        pass

    def initButton(self, buttonName, x, y, method) :
        button = QtWidgets.QPushButton(buttonName, self)
        button.setToolTip('es el caftoro {}'.format(buttonName))
        button.move(x,y)
        button.clicked.connect(method)
        return button

    def on_click(self):
        print('lol gadol')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())