import struct
def unpackOpenReq(msg):
     try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        arc_name, = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])
        msg = msg[name_len:]
        mail_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        mail, =  struct.unpack(">{}s".format(str(mail_len)),msg[:mail_len])
        msg = msg[mail_len:]
        pass_x, = struct.unpack(">QQQQ",msg[:32])
        msg = msg[32:]
        pass_y ,= struct.unpack(">QQQQQQQQ",msg[:64])
        return (arc_name,mail,pass_x,pass_y)  
     except Exception as e :
         print("error parsing, {}".format(e))
         return None 

def unpackMaster(msg):
    try:
        name_len, = struct.unpack(">L",msg[:4])
        msg = msg[4:]
        arc_name, = struct.unpack(">{}s".format(str(name_len)),msg[:name_len])
        msg = msg[name_len:]
        password = struct.unpack(">L",msg[:4])
        return (arc_name,password)
    except Exception as e:
        print("error parsing, {}".format(e))
        return None 

## changes to archive
   def masterCheck(self,password):
        return niv.md5(password) == self.password_md5
self.password_md5 = niv.md5(password)
  self.mail_list = mail_list

pass #not implemented - omri (authorization, drive to mail_list )
        if type(info_tup) is tuple:
            arc_name, password = info_tup
        if  arc_dict[arc_name].masterCheck:
            file_ids = drive_module.uplaod_to_drive(arc_dict[arc_name].file_list , [])
            drive_module.share(arc_dict[arc_name].mail_list,file_ids)

##changes to drive_module
def DeleteByFileId(file_id):
	try:
		DRIVE.files().delete(fileId=file_id).execute()
	except errors.HttpError, error:
		print("an error occured: %s", % error)
