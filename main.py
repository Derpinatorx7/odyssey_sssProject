import sys
import PyQt5.QtWidgets as QtWidgets

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
        
        self.show()
        
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