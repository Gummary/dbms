from parseSql import upperKetWord,rmNoUseChar
import os,hashlib,getpass
def md5(str):
    obj = hashlib.md5()
    obj.update(str)
    return obj.hexdigest()

_ALL_PERMISSION_ = ["GRANT","REVOKE","SELECT","INSERT","DELETE","UPDATE"]

class User():
    def __init__(self):
        self.userpermission = {}
        self.permission = {}
        self.passwd = {}
        self.pwdfile = None
        if not os.path.isfile(".passwd"):
            self.__set_root__()
        else:
            self.__user__()

    def __set_root__(self):
        print "Haven't dected the user root,please set the passwd of root:"
        passwd = getpass.getpass("passwd:")
        passwd = md5(passwd)
        self.passwd["root"] = passwd
        for permission in _ALL_PERMISSION_:
            self.permission[permission] = ["*"]
        self.userpermission["root"] = self.permission
        self.__update_user_()

    def __update_user_(self):
        self.pwdfile = open(".passwd","wb")
        for user in self.passwd.keys():
            data = user+"|"+self.passwd[user]
            permit = self.userpermission[user]
            for pname in permit:
                plist = permit[pname]
                data += "|" + pname +" " +"".join(plist)
            data +="\n"
            self.pwdfile.write(data)
        self.pwdfile.close()

    def __get_user_info__(self):
        self.pwdfile = open(".passwd","rb")
        while True:
            data = self.pwdfile.readline()
            if len(data) == 0:
                break
            data = data.strip("\n")
            data = data.split("|")
            while "" in data:
                data.remove("")
            username = data[0]
            userpasswd = data[1]
            self.passwd[username] = userpasswd
            data = data[2:]
            perdic = {}
            for per in data:
                pername = per.split(" ")[0]
                pertable = per.split(" ",1)[1]
                pertable = pertable.split(",")
                perdic[pername] = pertable
            self.userpermission[username] = perdic
        self.pwdfile.close()

    def __user__(self):
        self.__get_user_info__()
        while True:
            print "Select Operate:"
            print "1. Login\n2. Register"
            operate = raw_input()
            if operate == "1":
                username = raw_input("username:")
                if username not in self.passwd:
                    print "User not exists"
                    continue
                passwd = getpass.getpass("paswd:")
                passwd = md5(passwd)
                if passwd != self.passwd[username]:
                    print "Passwd Incorrect"
                    continue
                else:
                    self.permission = self.userpermission[username]
                    break
            elif operate == "2":
                username = raw_input("Input username:")
                if username in self.passwd:
                    print "User is already exist"
                    continue
                passwd = getpass.getpass("Input passwd:")
                passwd = md5(passwd)
                passwd2 = getpass.getpass("Input passwd again:")
                passwd2 = md5(passwd2)
                while passwd != passwd2:
                    print "The two passwords do not match"
                    passwd = getpass.getpass("Input passwd:")
                    passwd2 = getpass.getpass("Input passwd again:")
                    passwd = md5(passwd)
                    passwd2 = md5(passwd2)
                self.passwd[username] = passwd
                perdic = {"CREATE":[]}
                self.userpermission[username] = perdic
                self.permission = perdic
                self.__update_user_()
                break
            else:
                print "Wrong Input"



    def update_user(self,users,permissions):
        for user in users:
            if not user in self.passwd:
                print "User %s not exist"%user
                users.remove(user)
        for user in users:
            perdic = self.userpermission[user]
            l2 = []
            for per in permissions.keys():
                if perdic.get(per,None) == None:
                    perdic[per] = permissions[per]
                else:
                    plist = permissions[per]
                    plist = perdic[per].extend(plist)
                    plist = perdic[per]
                    l2 = list(set(plist))
                    l2.sort(key=plist.index)
                    perdic[per] = l2
                    self.userpermission[user] = perdic
        self.__update_user_()
        print self.userpermission


    def get_user_permissin(self):
        return self.permission

# if __name__ == "__main__":
#     u = User()
#     print u.get_user_permissin()
#     username = ["hepeng"]
#     permissions = {"SELECT":["STUDENT"],"INSERT":["STUDENT"],"UPDATE":["STUDENT"]}
#     u.update_user(username,permissions)
