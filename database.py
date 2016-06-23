from error import NODBSELE,NOSUCHDB,DBEXISTS,TABLEEXISTS,TABLENOTEXISTS
import re
from record import RecordHandle


def check_permission(Excep):
	def decorator(func):
		def wrapper(*args,**kw):
			if args[2]:
				return func(*args,**kw)
			else:
				raise Excep
		return wrapper
	return decorator

class DataBase():
	def __init__(self):
		self.use = False
		try:
			self.alldbfile = open(".alldb","rb+")
		except IOError, e:
			print "File not exists"
			self.alldbfile = open(".alldb","wb+")
		finally:
			self.alldb = self.alldbfile.readline().rstrip("\n")
		if len(self.alldb) != 0:
			self.alldb = self.alldb.split("|")
		else:
			self.alldb = []

	def __del__(self):
		self.alldbfile.close()

	def quit(self):
		self.__close_alldb__()

	def quitdb(self,dbname):
		self.alldbfile = open(".alldb","rb+")
		self.alldb = self.alldbfile.readline().rstrip("\n")
		if len(self.alldb) != 0:
			self.alldb = self.alldb.split("|")
		else:
			self.alldb = []
		self.use = False
		self.currentdb = None

	def creat_db(self,dbname):
		if dbname in self.alldb:
			raise DBEXISTS(dbname)

		self.alldb.append(dbname)
		file = open(dbname,"wb+")
		file.close()



	def use_db(self,dbname):
		if dbname not in self.alldb:
			raise NOSUCHDB(dbname)
		self.currentdb = dbname
		self.use = True
		dbfile = open(dbname,"rb+")
		byte = dbfile.readline().rstrip("\n")
		self.dbtables = []
		self.dbattrs = {}
		if len(byte)!=0:
			self.dbtables = byte.split("|")
		while True:
			byte = dbfile.readline().rstrip("\n")
			if len(byte) == 0:
				break
			tablename = byte.split("|")[0]
			tableattrs = byte.split("|")[1:]
			attrlist = []
			for attr in tableattrs:
				attrlist.append(attr.split(","))
			self.dbattrs[tablename] = attrlist
		self.__close_alldb__()
		dbfile.close()

	def del_db(self,dbname):
		if dbname in self.alldb:
			index = self.alldb.index(dbname)
			del self.alldb[index]
		else:
			raise NOSUCHDB(dbname)

	def __close_alldb__(self):
		data = "|".join(self.alldb)
		data+="\n"
		self.alldbfile.seek(0)
		self.alldbfile.write(data)
		self.alldbfile.flush()
		self.alldbfile.close()

	def show_alldb(self):
		if self.use:
			return

		print self.alldb


	def show_all_tables(self):
		if not self.use:
			return
		print self.dbtables
		print self.dbattrs


	@check_permission(NODBSELE)
	def __create_table__(self, tablename,permission,*attrs):
		if tablename in self.dbtables:
			raise TABLEEXISTS(tablename)

		self.dbtables.append(tablename)
		self.dbattrs[tablename] = attrs
		"""CreatFIle"""
		rcformat = attrs[-1][1]
		rchandle = RecordHandle(tablename,rcformat)
		rchandle.create_file()
		"""ENDCOMMENT"""
		self.__update_db_file_()


	@check_permission(NODBSELE)
	def __remove_table__(self,tablename,permission):
		if tablename not in self.dbtables:
			raise TABLENOTEXISTS
		index = self.dbtables[tablename]
		del self.dbtables[index]
		del self.dbattrs[tablename]
		self.__update_db_file_()


	def __update_db_file_(self):
		dbfile = open(self.currentdb,"wb+")
		data = "|".join(self.dbtables)
		data += "\n"
		dbfile.write(data)
		data = ""
		for key in self.dbattrs:
			attrs = self.dbattrs[key]
			data += key
			for item in attrs:
				data += "|%s" % ",".join(item)
			data +="\n"
			dbfile.write(data)
		dbfile.close()


	def create_table(self,tablename,*attrs):
		self.__create_table__(tablename,self.use,*attrs)

	def remove_table(self,tablename):
		self.__remove_table__(tablename,self.use)

	def has_table(self,tablename):
		if not self.use:
			raise NODBSELE

		if tablename in self.dbtables:
			return True
		else:
			return False

	def get_tableattrs(self,tablename):
		try:
			return self.dbattrs[tablename]
		except Exception,e:
			raise e

	def get_alldb(self):
		return self.alldb
