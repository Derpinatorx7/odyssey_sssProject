from user.pyc import *
import niv
import socket
buff = 4096
s = socket.socket()

loading_screen()
welcome_screen()


def upload_func():
    globals s, buff
    file_list = []
    mail_list = []
    for fil in tkFileDialog.askopenfilenames():
        file_list.append(fil.encode('ascii','ignore'))
    name = raw_input("your archive name: ")
    password = raw_input("your archive main password: ")
    if not password:
        password = niv.randomPassword()
    mail_list_len = input('how many people do you want to share the file with? ')
    for x in xrange(1,mail_list_len+1):
        mail_list.append(raw_input("user number {}'s mail".format(x)))
    required = input('number of people required to access the archive: ')
    msg = packSaveReq(name,password,mail_list,required)
    
    s.connect(("84.109.209.188",8080))
    while (msg):
        s.send(msg[:buff])
        msg = msg[buff:]
    s.close()


def startloop():
    print 'what would you like to do today? (upload or download)\n'   
    mode = raw_input('your choice: ')
    if mode = 'upload':
        upload_func()
    elif mode = 'download':
        download_func()
    else:
        print "we didn't understand your choice " #nisuah
        startloop()
    
startloop()



     
