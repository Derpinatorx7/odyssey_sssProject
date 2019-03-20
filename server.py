import niv
import socket
import struct
import hashlib
import smtplib
import datetime
import drive_module
import os
from sys import exit, argv as params
from os import system as cmd
from os.path import basename
import platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

print("please enter your mail and passowrd")
me = input("mail: \n")
while me[-10:] != "@gmail.com":
    print("gmail is reqired")
    me = input("mail: \n")
me_password = input("password: \n")
buff = 4096
s = socket.socket()
s.bind(("",8087))
s.listen(10)
unaltered_archive_dict = {}
arc_dict = {}
textFile = 'mailText.txt'
masterTextFile = 'masterMailText.txt'
need_to_delete = []

def deleteFile(f):
    if platform.system() == 'Linux':
        cmd('rm -rf {}'.format(f))
    elif platform.system() == 'Windows':
        cmd('del /q {}'.format(f))



class archive(object):
    def __init__(self, info_tup, password_list):
        file_list, arc_name, mail_list, password, required = info_tup
        self.name = arc_name
        self.account_dict = {} # mail: [sub_pass_md5ed (tuple (md5_x,md5_y)) , password_accepted? (bool)]
        self.mailList= mail_list
        for i,mail in enumerate(self.mailList):
            self.account_dict[mail] = [niv.tuple_md5(password_list[i]),0]
        self.password_md5 = niv.md5(password)
        self.mail_list = mail_list
        self.file_list = file_list
        self.required = required
        self.lastAccessed = datetime.datetime.now()
        self.AccessTimer = datetime.datetime.now()
        self.deleteTimer = None
        self.authorizedPasswordList = []
        self.fileId = []

    def authorizeUser(self, mail):
        self.account_dict[mail][1] = 1
        self.lastAccessed = datetime.datetime.now()

    def unauthorizeAll(self):
        for mail in self.mailList:
            self.account_dict[mail][1] = 0

    def masterCheck(self,password):
        return niv.md5(password) == self.password_md5
    
    def _countEntries(self):
        counter = 0
        for mail in self.account_dict:
            counter += self.account_dict[mail][1]
        return counter

    def canWeDecrypt(self):
        if self._countEntries() >= self.required:
            return True
        else:
            return False

    def startAccessTimer(self):
        self.AccessTimer = datetime.datetime.now()
    
    def updateAccessDetails(self):
        if datetime.datetime.now() - self.AccessTimer >= datetime.timedelta(minutes=30) or datetime.datetime.now() - self.lastAccessed >= datetime.timedelta(minutes=5):
            self.AccessTimer = datetime.timedelta(0)
            self.authorizedPasswordList = []
            self.unauthorizeAll()
    
    def checkPassword(self,mail, pass_tup):
        return self.account_dict[mail][0] == niv.tuple_md5(pass_tup)

    def savePassword(self, pass_tup):
        self.authorizedPasswordList.append(pass_tup)
    
    def tryToOpen(self):
        if self.canWeDecrypt():
            secret = niv.recover_secret(self.authorizedPasswordList)
            mailer(self, [secret], mode = 'master')
            fileDriveIDs = drive_module.upload_to_drive([self.name + '.zip'])
            self.fileId = fileDriveIDs
            authorized_list = []
            for x in self.account_dict:
                if self.account_dict[x][1] == 1:
                    authorized_list.append(x)
            drive_module.share(authorized_list,fileDriveIDs)
            deleteFile(self.name +'.zip')
            self.deleteTimer = datetime.datetime.now()
        else:
            print('cannot recover master, not enough passwords')
    


    def deleteFromDrive(self):
        for id in self.fileId:
            drive_module.DeleteByFileId(id)
        del(arc_dict[self.name])
        del(self)


def unpackOpenReq(msg):
     try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        arc_name = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])[0].decode("utf-8") 
        msg = msg[name_len:]
        mail_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        mail =  struct.unpack(">{}s".format(str(mail_len)),msg[:mail_len])[0].decode("utf-8") 
        msg = msg[mail_len:]
        pass_x = struct.unpack('>QQQQ',msg[:32])
        msg = msg[32:]
        pass_x = str(10**24*pass_x[0]+10**16*pass_x[1]+10**8*pass_x[2]+pass_x[3])
        pass_y = struct.unpack('>QQQQQQQQ',msg[:64])
        msg = msg[64:]
        pass_y = str(10**56*pass_y[0]+10**48*pass_y[1]+10**40*pass_y[2]+10**32*pass_y[3]+10**24*pass_y[4]+10**16*pass_y[5]+10**8*pass_y[6]+pass_y[7])
        pass_x = int(pass_x)
        pass_y = int(pass_y)
        return (arc_name,mail,pass_x,pass_y)  
     except Exception as e :
         print("error parsing, {}".format(e))
         return None 

def unpackMaster(msg):
    try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        arc_name = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])[0].decode("utf-8") 
        msg = msg[name_len:]
        password, = struct.unpack(">L",msg[:4])
        return (arc_name,password)
    except Exception as e:
        print("error parsing, {}".format(e))
        return None 

def unpackSaveReq(msg):
    try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]    
        password, = struct.unpack(">L",msg[:4])
        msg = msg[4:]    
        arc_name = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])[0].decode("utf-8") 
        msg = msg[name_len:]
        num_of_participants, = struct.unpack(">L", msg[:4])
        msg = msg[4:]
        mail_list = []
        print("40%")
        for i in range(num_of_participants):
            mail_len, = struct.unpack(">L",msg[:4])
            msg = msg[4:]    
            mail_list.append(struct.unpack(">{}s".format(str(mail_len)),msg[:mail_len])[0].decode("utf-8"))
            msg = msg[mail_len:]
        required, = struct.unpack(">L", msg[:4])
        msg = msg[4:]
        print('60%')
        num_of_files, = struct.unpack('>L',msg[:4])
        msg = msg[4:]
        arc_file_list= []
        print('starting to process files')
        for x in range(num_of_files):
            file_name_len, = struct.unpack('>L',msg[:4])
            msg = msg[4:]
            file_name = struct.unpack(">{}s".format(str(file_name_len)),msg[:file_name_len])[0].decode("utf-8") 
            msg = msg[file_name_len:]
            siz = struct.unpack('>QQQQQ',msg[:40])
            msg = msg[40:]
            siz = str(10**32*siz[0]+10**24*siz[1]+(10**16)*siz[2]+(10**8)*siz[3]+siz[4])
            siz = int(siz,2)
            file = open(file_name, 'wb')
            file.write(msg[:siz])
            file.close()
            arc_file_list.append(file_name)
            msg = msg[siz:]
        print("100%, files saved")
        return (arc_file_list, arc_name, mail_list, password,  required)
    except Exception as e:
        print(e)
        return None

def recieveMessage():
    global s
    msg = b''
    sc, address = s.accept()
    print(address)
    x = sc.recv(buff)
    while x:
        msg += x
        x = sc.recv(buff)
    if struct.unpack('>L',msg[:4])[0] == 0:
        info_tup = unpackSaveReq(msg[4:])
        mode = 'save'
    elif struct.unpack('>L',msg[:4])[0] == 1:
        info_tup = unpackOpenReq(msg[4:])
        mode = 'open'

    elif struct.unpack('>L',msg[:4])[0] == 2:
        info_tup = unpackMaster(msg[4:])
        mode = 'master'
    else:
        sc.send(b"lol u forked up (msg type invalid)")
    sc.close()
    return info_tup, mode

def sendMail(msg, reciever, arc_name):
    global me, me_password, arc_dict
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(me,me_password)
    mail.sendmail(me,reciever,msg.as_string())
    mail.close()
    print('mail sent to {} at {} +2:00GMT \narchive name: {}\nfiles: {}'.format(reciever, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), arc_name, ','.join(arc_dict[arc_name].file_list)))


def addtext(msg, text_file, password, arc_name, mode):
    fp = open(text_file, 'rb')
    if mode == 'subpass': msg.attach(MIMEText(fp.read().decode('utf-8') + arc_name + '\nyour password is: {}'.format(password)))
    elif mode == 'master': msg.attach(MIMEText(fp.read().decode('utf-8') + arc_name + '\nThe master password is: {}'.format(password)))
    fp.close()
    return msg


def setMessageParameters(reciever, arc_name, mode):
    global me
    msg = MIMEMultipart()
    if mode == 'subpass': msg['Subject'] = 'Your password for the archive: {}'.format(arc_name)
    elif mode == 'master': msg['Subject'] = 'Master password for the archive: {}'.format(arc_name)
    msg['From'] = me
    msg['To'] = reciever
    return msg

def mailer(archive, password_list, mode = 'subpass'):
    global textFile, masterTextFile
    for index,reciever in enumerate(archive.account_dict):
        msg = setMessageParameters(reciever, archive.name, mode)
        if mode == 'subpass': msg = addtext(msg, textFile, password_list[index], archive.name, mode)
        elif mode == 'master': msg = addtext(msg, masterTextFile, password_list[0], archive.name, mode)
        sendMail(msg, reciever, archive.name)

def periodicalEvents():
    for arc_name in arc_dict:
        if arc_dict[arc_name].lastAccessed:
            arc_dict[arc_name].deleteFromDrive     
        elif  arc_dict[arc_name]:
            if datetime.datetime.now() - arc_dict[arc_name].deleteTimer > datetime.timedelta(minutes=40) :
                arc_dict[arc_name].deleteFromDrive   #not implemented - delete file after week of not being used
    ##DeleteByFileID was added to drive module

def handleSaveReq(info_tup):
    global need_to_delete, unaltered_archive_dict, arc_dict
    if type(info_tup) is tuple:
        arc_file_list, arc_name, mail_list, password, required = info_tup
        if len(mail_list) > 0 and arc_name != "" and required > 0 and password > 0:
            unaltered_archive_dict[arc_name] = [mail_list, password, required]
    for name in unaltered_archive_dict:
        mail_list, password, required = unaltered_archive_dict[name]
        cmd(r'7za.exe a -p{} -y "{}.zip" {}'.format(password, name, " ".join(arc_file_list)))
        for fil in arc_file_list:
            deleteFile(fil)
        password_list = niv.createPasswords(*unaltered_archive_dict[name])
        arc_name = info_tup[1]
        arc_dict[arc_name] = archive(info_tup, password_list)
        mailer(arc_dict[arc_name],password_list)
        need_to_delete.append(name)

    for name in need_to_delete:
        del unaltered_archive_dict[name]

def handleOpenReq(info_tup):
    global arc_dict
    if type(info_tup) is tuple:
        arc_name, mail, password_x, password_y = info_tup
    if arc_dict[arc_name].checkPassword(mail,(password_x,password_y)):
        arc_dict[arc_name].updateAccessDetails()
        if arc_dict[arc_name].AccessTimer == datetime.timedelta(0):
            arc_dict[arc_name].startAccessTimer()
        arc_dict[arc_name].authorizeUser(mail)
        arc_dict[arc_name].savePassword((password_x,password_y))
        arc_dict[arc_name].lastAccessed = datetime.datetime.now()
        arc_dict[arc_name].tryToOpen()

def handleMaster(info_tup):
    if type(info_tup) is tuple:
        arc_name, password = info_tup
    if arc_dict[arc_name].masterCheck(password):
        print("unzipped:", arc_name)
        file_ids = drive_module.upload_to_drive([arc_dict[arc_name].name + '.zip'])
        drive_module.share(arc_dict[arc_name].mail_list,file_ids)
        mailer(arc_dict[arc_name], [password], mode = 'master')
        print("shared")
        deleteFile(arc_dict[arc_name].name +'.zip')
    else:
        print('wrong password')

def handleMessage():
    info_tup, mode = recieveMessage()
    if mode == 'save':
        handleSaveReq(info_tup)
    elif mode == 'open':
        handleOpenReq(info_tup)
    elif mode == 'master':
        handleMaster(info_tup)


      
while True:
    handleMessage()
    periodicalEvents()