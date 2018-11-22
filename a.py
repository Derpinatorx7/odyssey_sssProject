import struct
import os
import subprocess

def sevenzip(file_list, zipname, password):
    print("Password is: {}".format(password))
    for filename in file_list:
        system = subprocess.Popen(["7z", "a", zipname, filename, "-p{}".format(password)])
        system.communicate()

sevenzip(["hw1_213743818.pdf","hw2_213743818.pdf"],'d',9999)