from error import NODBSELE,NOSUCHDB,DBEXISTS,TABLEEXISTS,TABLENOTEXISTS,ATTRNOTEXISTS,ExceedLimit,NONEVALUE
import re,struct
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

	def do_select(self,sqldic):
		tablename = sqldic["FROM"][0]
		rchandle = new RecordHandle()
		attrformat = self.dbattrs[tablename][-1][1]
		rchandle.open_file(tablename,attrformat)
		rchandle.show_all_record()




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

	def check_table(self,tables):
		for table in tables:
		    if not self.has_table(table):
				raise TABLENOTEXISTS(table)
		return True

	def checkSelect(self,selects,tables):
	    for i in range(len(selects)):
	        select = selects[i]
	        if "*" in select[0]:
	            continue
	        findTable = self.isInTable(select[0],tables)
	        if findTable == None:
	            raise ATTRNOTEXISTS(select[0])
	        selects[i][0] =findTable+"."+select[0].upper()
	    return selects


	def checkWhere(self,wheres,tables):
		if wheres == None:
		    return None
		length = len(wheres)
		i = 0
		while i < length:
		    where = wheres[i]
		    findTable = self.isInTable(where[0],tables)
		    if findTable == None:
		        raise ATTRNOTEXISTS(where[0])
		    wheres[i][0] =findTable+"."+where[0].upper()
		    findTable = isInTable(where[2].upper(),tables,meta)
		    if findTable != None:
		        where[2] =findTable+"."+where[2].upper()
		        wheres.pop(i)
		        wheres.append(where)
		        i -= 1
		        length = length - 1
		    i += 1
	return wheres

	def checkGroup(self,groups,tables):
    if groups == None:
        return None
    for i in range(len(groups)):
        findTable = self.isInTable(groups[i],tables)
        if findTable == None:
            raise ATTRNOTEXISTS(group[i])
        groups[i] = findTable+"."+groups[i]
    return groups

	def checkOrder(self,orders,tables):
    if orders ==None:
        return None
    for i in range(len(orders)):
        findTable = self.isInTable(orders[i][0],tables)
        if findTable == None:
            raise ATTRNOTEXISTS(orders[i][0])
        orders[i][0] = findTable+"."+orders[i][0]
    return orders

	def isInTable(self,attr,tables):
		for table in tables:
			attrs = self.get_tableattrs(table)
			for a in attrs:
				if attr in attrs:
					return table
		return None


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


	def insert_record(self,tablename,values):
		if not self.use:
			raise NODBSELE

		if not self.has_table(tablename):
			raise TABLENOTEXISTS(tablename)

		attrformat = self.dbattrs[tablename][-1][1]
		attrs = self.get_tableattrs(tablename)
		data = []
		if isinstance(values,dict):
			allkey = values.keys()
			for key in allkey:
				flag = False
				for attr in attrs:
					if key == attr[0]:
						flag = True
						break
				if not flag:
					raise ATTRNOTEXISTS(key)
			limit = attrformat.split("s")
			while "" in limit:
				limit.remove("")
			index = 0
			for attr in attrs:
				valuename = attr[0]
				valuelen = attr[1]
				if valuename == "__format__":
					continue
				l = int(limit[index])
				index+=1
				if "PRIMARY KEY" in attr or "NOT NULL" in attr:
					if valuename not in values:
						raise NONEVALUE(valuename)
				if valuename in values:
					if len(values[valuename]) > l:
						raise ExceedLimit
					data.append(values[valuename])
				else:
					data.append("\x00")
		elif isinstance(values,list):
			data = values
		else:
			raise Exception("Unkonw Value")
		rchandle = RecordHandle()
		rchandle.open_file(tablename,attrformat)
		rchandle.insert_record(data)
		rchandle.close_file()
