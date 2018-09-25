import niv
import socket
import struct
import hashlib
import smtplib
import sys
import datetime
from os import system as cmd
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

me = 'your mail'
me_password = 'your mail password'
buff = 4096
s = socket.socket()
s.bind(("",8080))
s.listen(10)
unaltered_archive_dict = {}
arc_list = {}
textFile = 'mailtext.txt'
need_to_delete = []


class archive(object):
    def __init__(self, info_tup, password_list):
        file_list, arc_name, mail_list, password, required = info_tup
        self.name = arc_name[:-4]
        self.account_list = {} # mail: [sub_pass_md5ed, sent_password]
        for i,mail in enumerate(mail_list):
            self.account_list[mail] = [niv.md5(password_list[i]),0]
        self.password = password
        self.file_list = file_list
        self.required = required
        self.timer = None
    
    def authorize(self, mail):
        self.account_list[mail][1] = 1

    def count_entries(self):
        counter = 0
        for mail in self.account_list:
            counter += self.account_list[mail][1]
        return counter

    def can_we_decrypt(self):
        if self.count_entries() >= self.required:
            return True
        else:
            return False


def unpackSaveReq(msg):
    try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]    
        password, = struct.unpack(">L",msg[:4])
        msg = msg[4:]    
        arc_name, = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])
        msg = msg[name_len:]
        num_of_participants, = struct.unpack(">L", msg[:4])
        msg = msg[4:]
        mail_list = []
        print "40%"
        for i in range(num_of_participants):
            mail_len, = struct.unpack(">L",msg[:4])
            msg = msg[4:]    
            mail_list.append(struct.unpack(">{}s".format(str(mail_len)),msg[:mail_len])[0])
            msg = msg[mail_len:]
        required, = struct.unpack(">L", msg[:4])
        msg = msg[4:]
        print '60%'
        num_of_files, = struct.unpack('>L',msg[:4])
        msg = msg[4:]
        arc_file_list= []
        print 'starting to process files'
        for x in range(num_of_files):
            file_name_len, = struct.unpack('>L',msg[:4])
            msg = msg[4:]
            file_name, = struct.unpack(">{}s".format(str(file_name_len)),msg[:file_name_len])
            msg = msg[file_name_len:]
            siz = struct.unpack('>QQQQQ',msg[:40])
            msg = msg[40:]
            siz = '0b'+ str(10**32*siz[0]+10**24*siz[1]+(10**16)*siz[2]+(10**8)*siz[3]+siz[4])
            siz = int(siz,2)
            file = open(file_name, 'wb')
            file.write(msg[:siz])
            file.close()
            arc_file_list.append(file_name)
            msg = msg[siz:]
        print "100%, files saved"
        return (arc_file_list, arc_name, mail_list, password,  required)
    except Exception as e:
        print e
        return None

def recieveMessage():
    global s
    msg = ''
    sc, address = s.accept()
    print address
    x = sc.recv(buff)
    while x:
        msg += x
        x = sc.recv(buff)
    info_tup = unpackSaveReq(msg)
    sc.close()
    return info_tup

def sendMail(msg, reciever, arc_name):
    global me, me_password, arc_file_list
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(me,me_password)
    mail.sendmail(me,reciever,msg.as_string())
    mail.close()
    print 'mail sent to {} at {} +2:00GMT \narchive name: {}\nfiles: {}'.format(reciever, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), arc_name, ','.join(arc_file_list))


def addtext(msg, text_file, sub_password, arc_name):
    fp = open(text_file, 'rb')
    msg.attach(MIMEText(fp.read() + str(arc_name) + '\nyour passwrd is: {}'.format(sub_password)))
    fp.close()
    return msg


def setMessageParameters(reciever, arc_name):
    global me
    msg = MIMEMultipart()
    msg['Subject'] = 'Your password for the archive: {}'.format(arc_name)
    msg['From'] = me
    msg['To'] = reciever
    return msg

def mailer(archive, password_list):
    global textFile
    for reciever in archive.account_list:
        msg = setMessageParameters(reciever, archive.name)
        msg = addtext(msg, textFile, archive.account_list[reciever][0], archive.name)
        sendMail(msg, reciever, archive.name)


while True:
    info_tup = recieveMessage()
    if type(info_tup) is tuple:
        arc_file_list, arc_name, mail_list, password, required = info_tup
        if len(mail_list) > 0 and arc_name != "" and required > 0 and password > 0:
            unaltered_archive_dict[arc_name] = [mail_list, password, required]
    for name in unaltered_archive_dict:
        mail_list, password, required = unaltered_archive_dict[name]
        cmd(r'7zip\7za a -p{} -y {}.zip {}'.format(password, name[:name.index('.')], " ".join(arc_file_list)))
        for fil in arc_file_list:
           cmd("del "+fil)
        password_list = niv.createPasswords(*unaltered_archive_dict[name])
        arc_name = info_tup[1][:-4]
        arc_list[arc_name] = archive(info_tup, password_list)
        mailer(arc_list[arc_name], password_list)
        need_to_delete.append(name)

    for name in need_to_delete:
        del unaltered_archive_dict[name]
    need_to_delete=[]
    password_list=[]
    mail_list=[]
    password=[]
    infotup=()


