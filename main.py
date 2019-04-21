import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import user

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
        mainLayout.addWidget(self.initButton("upload",70,10, self.showUploadView,BUTTONSTYLESHEET), 1, 0)
        mainLayout.addWidget(self.initButton("download",10,70, self.hideCurrentView,BUTTONSTYLESHEET), 1, 1)
        mainLayout.addWidget(self.initButton("master download",40,100, self.hideCurrentView,BUTTONSTYLESHEET), 1, 2)
        self.mainView.setLayout(mainLayout)

        self.mainView.setParent(self)


    def initUploadView(self):
        self.uploadView = QtWidgets.QFrame()
        uploadLayout = QtWidgets.QGridLayout()
        arcName = self.initTextBox('Archive name',70,10)
        password = self.initTextBox('Main password',10,70)
        Email = self.initTextBox('E-Mails',40,100)
        required = self.initTextBox('required amount of people to access files',10,70)
        self.files = []
        uploadLayout.addWidget(arcName,0,0)
        uploadLayout.addWidget(password,0,1)
        uploadLayout.addWidget(Email,0,2)
        uploadLayout.addWidget(required,1,1)
        uploadLayout.addWidget(self.initButton("select files",70,10, self.fileChooser,BUTTONSTYLESHEET), 1, 0)
        uploadLayout.addWidget(self.initButton("submit",70,10,self.submitUploadRequest,BUTTONSTYLESHEET),2,2)
        self.UploadTextBoxes = [arcName,password,Email,required]
        self.uploadView.setLayout(uploadLayout)

    def fileChooser(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.files = files 

    def submitUploadRequest(self):
        if not self.files: raise FileNotFoundError
        password = int(self.UploadTextBoxes[1].text()) if \
        self.UploadTextBoxes[1].text() else user.randomPassword()  
        msg = user.packSaveReq(self.UploadTextBoxes[0].text(),\
            password,self.UploadTextBoxes[2].text().split('\n'),\
                self.UploadTextBoxes[3].text(),self.files)
        user.handleMsg(msg);

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

    
    def initTextBox(self,boxName,x,y):
        tBox = QtWidgets.QLineEdit(self)
        tBox.setToolTip('es el boxo {}'.format(boxName))
        tBox.move(20, 20)
        tBox.resize(280,40)
        return tBox

    def initButton(self, buttonName, x, y, method, styleSheet):
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