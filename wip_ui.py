import user
import niv
import socket
from tkinter import filedialog
buff = 4096
s = socket.socket()

loading_screen() #not implemented
welcome_screen() #not implemented


def upload_func():
    global s, buff
    file_list = []
    mail_list = []
    for fil in filedialog.askopenfilenames():
        file_list.append(fil.encode('ascii','ignore'))
    name = input("your archive name: ")
    password = input("your archive main password: ")
    if not password:
        password = niv.randomPassword()
    mail_list_len = int(input('how many people do you want to share the file with? '))
    for x in range(1,mail_list_len+1):
        mail_list.append(input("user number {}'s mail".format(x)))
    required = int(input('number of people required to access the archive: '))
    msg = user.packSaveReq(name,password,mail_list,required)
    
    s.connect(("84.109.209.188",8080))
    while (msg):
        s.send(msg[:buff])
        msg = msg[buff:]
    s.close()

def download_func(mode = 1):
    global s, buff
    if mode == 1:
        name = input("your archive name: ")
        mail = input("your mail: ")
        passtup = input("your password tupple(as it was sent to you): ")
        msg = user.packOpenReq(name,mail,passtup)
    else:
        name = name = input("your archive name: ")
        password = input("please enter the main password: ")
        msg = user.MasterOpen(name,password)

    s.connect(("84.109.209.188",8080))
    while (msg):
        s.send(msg[:buff])
        msg = msg[buff:]
    s.close()


def startloop():
    print('what would you like to do today? (upload, try to download or use the master password to download?)\n')   
    mode = input('your choice: ')
    if mode == 'upload':
        upload_func()
    elif mode == 'download':
        download_func() #not implemented
    elif mode == 'master download'
        download_func(2)
    else:
        print("we didn't understand your choice ") #nisuah
        startloop()
    
startloop()



     
