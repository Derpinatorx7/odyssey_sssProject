import sys
import os
import socket
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import user

BUFFER = 4096
LOCKDOWNYELLOW = QtGui.QColor(254,226,1) ## to be changed
LOCKDOWNGRAY = QtGui.QColor(122,128,130)
LOCKDOWNBLACK = QtGui.QColor(0,0,0)

BUTTONSTYLESHEET = \
    '''QPushButton {background-color: rgb(254,226,1);
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: rgb(254,226,1);
    font: bold 14px;
    color: rgb(122,128,130);
    min-width: 10em;
    padding: 6px;}
    QPushButton:pressed {
    border-color: rgb(224,196,0);
    background-color: rgb(224,196,0);
    color: rgb(0,0,0);
    border-style: inset;}'''

LABELSTYLESHEET = \
    '''border: 10px solid;
    border-color: rgb(100,137,167);
    border-radius: 20px;
    font: bold 8pt "Open Sans";
    text-align: center;
    color: rgb(0,0,0);
    background-color: rgb(100,137,167);
    '''

LINEEDITSTYLESHEET = \
    '''border: 5px solid;
    border-color: rgb(255, 255, 255);
    border-radius: 10px;
    font: bold 8pt "Open Sans";
    text-align: center;
    border-color: rgb(0,0,0);
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);'''


##########
# Consts #
##########
SCALAR = 1.4
PORT = 8088
IP = "127.0.0.1" 
BACKGROUND_FILE = os.path.join(os.getcwd(),"bg.jpg")
LOGO_FILE = os.path.join(os.getcwd(),"logoVert.png")


class App(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'LockDown'
        self.left = 10
        self.top = 10
        self.width = 640 * SCALAR
        self.height = 480 * SCALAR
        self.currentView = "main"
        self.downloadEdits = {}
        self.masterDownloadEdits = {}
        self.uploadEdits = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.initMainView()
        self.initUploadView()
        self.initDownloadView()
        self.initMasterDownloadView()

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setBackground(BACKGROUND_FILE)

        self.show()
        
    def setBackground(self,background):
        oImage = QtGui.QImage(background)                   
        #sImage = oImage.scaled(QtCore.QSize(self.width,self.height))    # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(oImage))                      # 10 = Windowrole
        self.setPalette(palette)

    def initMainView(self):
        global BUTTONSTYLESHEET
        self.mainView = QtWidgets.QFrame()
        mainLayout = QtWidgets.QGridLayout()
        
        self.addSpacer(mainLayout,3,5)
        mainLayout.addItem(QtWidgets.QSpacerItem(self.width / 6,20),0,0)

        logo = QtWidgets.QLabel("logoLabel")
        logo.resize(560,280)
        pic = QtGui.QPixmap(LOGO_FILE)
        logo.setPixmap(pic.scaled(logo.size()))
        
        mainLayout.addWidget(logo,1,1)

        mainLayout.addWidget(
            self.initButton(
                "upload",70,10,self.showUploadView,BUTTONSTYLESHEET,
                text="open the upload window"),
                4, 1
                )
        
        mainLayout.addWidget(
            self.initButton(
                "download",10,70, self.showDownloadView,BUTTONSTYLESHEET,
                text = "open the download winodw"),
                5, 1
                )
        
        mainLayout.addWidget(
            self.initButton(
                "master download",40,100, self.showMasterDownloadView,BUTTONSTYLESHEET,
                text = "open the master download window"),
                6, 1
                )
        
        self.mainView.setLayout(mainLayout)
        self.mainView.setParent(self)

    def initUploadView(self):
        global LABELSTYLESHEET, LINEEDITSTYLESHEET, BUTTONSTYLESHEET
        self.uploadView = QtWidgets.QFrame()
        uploadLayout = QtWidgets.QGridLayout()

        self.addSpacer(uploadLayout,0,10)
        uploadLayout.addItem(QtWidgets.QSpacerItem(self.width / 2.4,50),0,2)
        uploadLayout.addItem(QtWidgets.QSpacerItem(self.height / 3,20),0,1)
        

        #nameLabel = QtWidgets.QLabel("uploadLabel")
        #nameLabel.setText("Enter archive name")
        #nameLabel.setStyleSheet(LABELSTYLESHEET)
        #uploadLayout.addWidget(nameLabel,1,1)
        
        nameEdit = QtWidgets.QLineEdit("archive name")
        nameEdit.setText("Archive name")
        nameEdit.setStyleSheet(LINEEDITSTYLESHEET)
        nameEdit.setToolTip('the name your archive will be known as in our system')
        self.uploadEdits["nameEdit"] = nameEdit
        uploadLayout.addWidget(nameEdit, 2, 1)
        #uploadLayout.addItem(QtWidgets.QSpacerItem(0, 100),2,1)
        
        #uploadLabel = QtWidgets.QLabel("uploadLabel")
        #uploadLabel.setText("Enter Main password")
        #uploadLabel.setStyleSheet(LABELSTYLESHEET)
        #uploadLayout.addWidget(uploadLabel,3,1)
        
        passwordEdit = QtWidgets.QLineEdit("password")
        passwordEdit.setText("Main password")
        passwordEdit.setStyleSheet(LINEEDITSTYLESHEET)
        passwordEdit.setToolTip('the password you can use to directly access the archive')
        self.uploadEdits["passwordEdit"] = passwordEdit
        uploadLayout.addWidget(passwordEdit, 3, 1)
        #uploadLayout.addItem(QtWidgets.QSpacerItem(0, 100),4,1)

        #kLabel = QtWidgets.QLabel("kLabel")
        #kLabel.setText("enter the amount of people required to access the archive")
        #kLabel.setStyleSheet(LABELSTYLESHEET)
        #kLabel.setWordWrap(True)
        #uploadLayout.addWidget(kLabel,2,1)
        
        kEdit = QtWidgets.QLineEdit("the amout of people required to access the archive")
        kEdit.setText("num of passwords required")
        kEdit.setStyleSheet(LINEEDITSTYLESHEET)
        kEdit.setToolTip('the amount of subpassword you need to access the archive')
        self.uploadEdits["kEdit"] = kEdit
        uploadLayout.addWidget(kEdit, 4, 1)

        uploadLayout.addWidget(
        self.initButton
            (
                "Choose files",0,0,self.fileChooser,BUTTONSTYLESHEET,
                text = "this button will open a file choosing dialog, choose the files you want in the archive"
            )
            ,6,3)

        uploadLayout.addWidget(
        self.initButton
            (
                "E-mail list file",0,0,self.mailChooser,BUTTONSTYLESHEET,
                text = "this button will open a file choosing dialog, choose the .txt file that has the email list, seperated by lines"
            )
            ,5,3)

        uploadLayout.addWidget(
            self.initButton
            (
                "submit",0,0,self.sendUploadReq,BUTTONSTYLESHEET,
                text = "this button will send all the info you gave us, so make sure everything is correct"
            )
            ,7,3)
        self.files = []
        self.mailFile = ""

        uploadLayout.addWidget(
            self.initButton
            (
                "Back",0,0,self.showMainView,BUTTONSTYLESHEET,
                text = "this button will go back to the main window"
            )
            ,7,1)

        self.uploadView.setLayout(uploadLayout)

    def initDownloadView(self):
        global LABELSTYLESHEET, LINEEDITSTYLESHEET, BUTTONSTYLESHEET
        self.downloadView = QtWidgets.QFrame()
        downloadLayout = QtWidgets.QGridLayout()
        
        self.addSpacer(downloadLayout,0,8)
        downloadLayout.addItem(QtWidgets.QSpacerItem(self.width / 3.8,20),0,3)
        #nameLabel = QtWidgets.QLabel("downloadLabel")
        #nameLabel.setText("Enter arcname")
        #nameLabel.setStyleSheet(LABELSTYLESHEET)
        #downloadLayout.addWidget(nameLabel,1,1)
        
        nameEdit = QtWidgets.QLineEdit("archive name")
        nameEdit.setText("archive name")
        nameEdit.setStyleSheet(LINEEDITSTYLESHEET)
        nameEdit.setToolTip("the name of the archive your are trying to open")
        self.downloadEdits["nameEdit"] = nameEdit
        downloadLayout.addWidget(nameEdit, 2, 1)

        #downloadLabel = QtWidgets.QLabel("downloadLabel")
        #downloadLabel.setText("Enter Email")
        #downloadLabel.setStyleSheet(LABELSTYLESHEET)
        #downloadLayout.addWidget(downloadLabel,3,1)

        emailEdit = QtWidgets.QLineEdit("email")
        emailEdit.setText("mail@example.com")
        emailEdit.setStyleSheet(LINEEDITSTYLESHEET)
        emailEdit.setToolTip("enter your mail to make sure it's the correct subpassword")
        self.downloadEdits["emailEdit"] = emailEdit
        downloadLayout.addWidget(emailEdit, 3, 1)
        downloadLayout.addItem(QtWidgets.QSpacerItem(0, 100),4,1)

        xEdit = QtWidgets.QLineEdit("Enter password x coordinate")
        xEdit.setText("X Coordinate")
        xEdit.setStyleSheet(LINEEDITSTYLESHEET)
        yEdit = QtWidgets.QLineEdit("Enter password y coordinate")
        yEdit.setText("Y Coordinate")
        yEdit.setStyleSheet(LINEEDITSTYLESHEET)
        self.downloadEdits["xEdit"] = xEdit
        downloadLayout.addWidget(xEdit, 4, 1)
        self.downloadEdits["yEdit"] = yEdit
        downloadLayout.addWidget(yEdit, 4, 2)

        #passwordLabel = QtWidgets.QLabel("passwordLabel")
        #passwordLabel.setText("enter x and y coordinates")
        #passwordLabel.setStyleSheet(LABELSTYLESHEET)
        #self.downloadEdits["passwordLabel"] = passwordLabel
        
        #downloadLayout.addWidget(passwordLabel,5,2)

        downloadLayout.addWidget(
            self.initButton
            (
                "submit",0,0,self.sendOpenReq,BUTTONSTYLESHEET,
                text = "this button will send all the info you gave us, so make sure everything is correct"
            )
                ,7,4)

        downloadLayout.addWidget(
            self.initButton
            (
                "Back",0,0,self.showMainView,BUTTONSTYLESHEET,
                text = "this button will go back to the main window"
            )
            ,7,1)
            

        self.downloadView.setLayout(downloadLayout)

    def initMasterDownloadView(self):
        global LABELSTYLESHEET, LINEEDITSTYLESHEET, BUTTONSTYLESHEET
        self.masterDownloadView = QtWidgets.QFrame()
        masterDownloadLayout = QtWidgets.QGridLayout()
        
        self.addSpacer(masterDownloadLayout,0,10)
        masterDownloadLayout.addItem(QtWidgets.QSpacerItem(self.width / 2.15,110),0,2)

        #nameLabel = QtWidgets.QLabel("nameLabel")
        #nameLabel.setText("Enter arcname")
        #nameLabel.setStyleSheet(LABELSTYLESHEET)
        #masterDownloadLayout.addWidget(nameLabel,1,1)

        nameEdit = QtWidgets.QLineEdit("archive name")
        nameEdit.setText("archive name")
        nameEdit.setStyleSheet(LINEEDITSTYLESHEET)
        nameEdit.setToolTip("the name of the archive your are trying to open")
        self.masterDownloadEdits["nameEdit"] = nameEdit
        masterDownloadLayout.addWidget(nameEdit, 2, 1)
        
        #masterPasswordLabel = QtWidgets.QLabel("masterPasswordLabel")
        #masterPasswordLabel.setText("Master Password")
        #masterPasswordLabel.setStyleSheet(LABELSTYLESHEET)
        #masterDownloadLayout.addWidget(masterPasswordLabel,3,1)

        masterPasswordEdit = QtWidgets.QLineEdit("masterPasswordEdit")
        masterPasswordEdit.setText("Master Password")
        masterPasswordEdit.setStyleSheet(LINEEDITSTYLESHEET)
        masterPasswordEdit.setToolTip("the password you entered when sending us the files in this archive")
        self.masterDownloadEdits["masterPasswordEdit"] = masterPasswordEdit
        masterDownloadLayout.addWidget(masterPasswordEdit, 3, 1)


        masterDownloadLayout.addWidget(
            self.initButton
            (
                "submit",0,0,self.sendOpenReq,BUTTONSTYLESHEET,
                text = "this button will send all the info you gave us, so make sure everything is correct"
            )
                ,7,3)

        masterDownloadLayout.addWidget(
            self.initButton
            (
                "Back",0,0,self.showMainView,BUTTONSTYLESHEET,
                text = "this button will go back to the main window"
            )
            ,7,1)

        self.masterDownloadView.setLayout(masterDownloadLayout)

    def fileChooser(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.files = files 
        else:
            QtWidgets.QMessageBox.warning(self,"","No files were chosen")

    def mailChooser(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        mailFile, _ = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if mailFile:
            if 1 < len(mailFile):
                QtWidgets.QMessageBox.warning(self,"Too many files were chosen")
            self.mailFile = mailFile[0]
        else:
            QtWidgets.QMessageBox.warning(self,"","No files were chosen")
    
    def sendUploadReq(self):
        global BUFFER
        
        if not self.files or not self.mailFile.endswith(".txt") : raise FileNotFoundError
        print(self.files)
        password = user.randomPassword(password=int(self.uploadEdits["passwordEdit"].text()))
        name = self.uploadEdits["nameEdit"].text()
        mailList = open(self.mailFile).read().split('\n')
        k = int(self.uploadEdits["kEdit"].text())
        msg = user.packSaveReq(name,password,mailList,k,self.files)
        
        s = socket.socket()
        s.connect((IP,PORT))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

        self.showMainView()
        
    def sendOpenReq(self):
        global BUFFER
        msg = user.packOpenReq(self.downloadEdits["nameEdit"].text(),self.downloadEdits["emailEdit"].text(),(int(self.downloadEdits["xEdit"].text()),int(self.downloadEdits["yEdit"].text())))
        
        s = socket.socket()
        s.connect((IP,PORT))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

        self.showMainView()

    def sendMasterOpenReq(self):
        global BUFFER
        msg = user.packMasterOpen(self.masterDownloadEdits["nameEdit"].text(),self.masterDownloadEdits["masterPasswordEdit"])
        
        s = socket.socket()
        s.connect((IP,PORT))
        while (msg):
            s.send(msg[:BUFFER])
            msg = msg[BUFFER:]
        s.close()

        self.showMainView()

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
        self.mainView.setParent(self)
        self.mainView.show()
    
    def initTextBox(self,boxName,x,y):
        tBox = QtWidgets.QLineEdit(self)
        tBox.setToolTip('es el boxo {}'.format(boxName))
        tBox.move(20, 20)
        tBox.resize(280,40)
        return tBox

    def initButton(self, buttonName, x, y, method, styleSheet,text = None):
        button = QtWidgets.QPushButton(buttonName, self)
        if not text:
            button.setToolTip('es el caftoro {}'.format(buttonName))
        else:
            button.setToolTip(text) 
        button.move(x,y)
        button.clicked.connect(method)
        button.setStyleSheet(styleSheet)
        return button

    def addSpacer(self,layout,start,numberOfSpacers):
        for i in range(numberOfSpacers):
            layout.addItem(QtWidgets.QSpacerItem(10,75),start + i,0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())