import sys
import socket
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
BUFFER = 4096
import user

LOCKDOWNYELLOW = "rgb(254,226,1)"

BUTTONSTYLESHEET = '''QPushButton {background-color: rgb(254,226,1);
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px;}
    QPushButton:pressed {
    background-color: RGB(204, 182, 159);
    border-style: inset;}'''

LABELSTYLESHEET = '''border: 10px solid;
border-color: rgb(254,226,1);
border-radius: 20px;
font: bold 8pt "Open Sans";
text-align: center;
color: rgb(254,226,1);
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
OG_BACKGROUND_FILE = "test.jpg"
DOWNLOAD_BACKGROUND_FILE = "background.png"
UPLOAD_BACKGROUND_FILE = "background.png"

class App(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'LockDown'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.currentView = "main"
        self.downloadEdits = {}
        self.masterDownloadEdits = {}
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
        msg = user.packOpenReq(self.downloadEdits["nameEdit"].text(),self.downloadEdits["emailEdit"].text(),(int(self.downloadEdits["xEdit"].text()),int(self.downloadEdits["yEdit"].text())))
        
        s = socket.socket()
        s.connect(("127.0.0.1",8087))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

    def sendMasterOpenReq(self):
        global BUFFER
        msg = user.packMaster(self.masterDownloadEdits["nameEdit"].text(),self.masterDownloadEdits["masterPasswordEdit"])
        
        s = socket.socket()
        s.connect(("127.0.0.1",8087))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

    def initMasterDownloadView(self):
        global LABELSTYLESHEET, LINEEDITSTYLESHEET, BUTTONSTYLESHEET
        self.masterDownloadView = QtWidgets.QFrame()
        masterDownloadLayout = QtWidgets.QGridLayout()
        masterDownloadLayout.addItem(QtWidgets.QSpacerItem(10,30),0,0)
        nameLabel = QtWidgets.QLabel("nameLabel")
        nameLabel.setText("Enter arcname")
        nameLabel.setStyleSheet(LABELSTYLESHEET)
        masterDownloadLayout.addWidget(nameLabel,1,1)
        nameEdit = QtWidgets.QLineEdit("archive name")
        nameEdit.setText("archive name")
        nameEdit.setStyleSheet(LINEEDITSTYLESHEET)
        
        self.masterDownloadEdits["nameEdit"] = nameEdit
        masterDownloadLayout.addWidget(nameEdit, 1, 2)
        masterDownloadLayout.addItem(QtWidgets.QSpacerItem(0, 100),2,1)
        mailLabel = QtWidgets.QLabel("mailLabel")
        mailLabel.setText("Email")
        mailLabel.setStyleSheet(LABELSTYLESHEET)
        masterDownloadLayout.addWidget(mailLabel,3,1)

        mailEdit = QtWidgets.QLineEdit("mailEdit")
        mailEdit.setText("enter your mail")
        mailEdit.setStyleSheet(LINEEDITSTYLESHEET)
        self.masterDownloadEdits["emailEdit"] = mailEdit
        masterDownloadLayout.addWidget(mailEdit, 3, 2)
        masterDownloadLayout.addItem(QtWidgets.QSpacerItem(0, 100),4,1)

        masterPasswordLabel = QtWidgets.QLabel("masterPasswordLabel")
        masterPasswordLabel.setText("Master Password")
        masterPasswordLabel.setStyleSheet(LABELSTYLESHEET)
        masterDownloadLayout.addWidget(masterPasswordLabel,5,1)

        masterPasswordEdit = QtWidgets.QLineEdit("masterPasswordEdit")
        masterPasswordEdit.setText("enter your Paswword")
        masterPasswordEdit.setStyleSheet(LINEEDITSTYLESHEET)
        self.masterDownloadEdits["masterPasswordEdit"] = masterPasswordEdit
        masterDownloadLayout.addWidget(masterPasswordEdit, 5, 2)
        masterDownloadLayout.addItem(QtWidgets.QSpacerItem(20, 20),6,3)

        masterDownloadLayout.addWidget(self.initButton("submitButton",0,0,self.sendMasterOpenReq,BUTTONSTYLESHEET),7,4)
        
        self.masterDownloadView.setLayout(masterDownloadLayout)

 
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
        self.masterDownloadView.setParent(self)
        self.mainView.show()
    
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