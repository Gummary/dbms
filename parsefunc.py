from parseSql import parse,upperKetWord,rmNoUseChar
from error import SYNTAXERROR,TABLENOTEXISTS,TYPEERROR
import re

def getFormat(*attrs):
	rcformat = ""
	for attr in attrs:
		valuetype = attr[1]
		if "INT" == valuetype:
			rcformat += "10s"
		elif "FLOAT" == valuetype:
			rcformat += "10s"
		elif "CHAR" in valuetype:
			pattern = "CHAR\((\d+)\)"
			pattern = re.compile(pattern,re.S)
			value = re.findall(pattern,valuetype)[0]
			rcformat+="%ds"%int(value)
		else:
			raise TYPEERROR(valuetype)
	return rcformat


@parse("SELECT")
def SeltctParse(dbhandle,sql):
	pass

@parse("HELP")
def HelpParse(dbhandle,sql):
	if "HELP DATABASE" in sql:
		alldb = dbhandle.get_alldb()
		print " ".join(alldb)
	elif "HELP TABLE" in sql:
		tables = sql.split(" ")[2:]
		while '' in tables:
   			tables.remove('')
		for table in tables:
			try:
				if dbhandle.has_table(table):
					attrlist = dbhandle.get_tableattrs(table)
					print "Table %s:"%table
					for attr in attrlist:
						if attr[0] == "__format__":
							continue
						print attr[0]+":"+" ".join(attr[1:])
				else:
					raise TABLENOTEXISTS(table)
			except Exception, e:
				print e
				continue
	else:
		raise SYNTAXERROR

@parse("USE")
def UseParse(dbhandle,sql):
	db = sql.split(" ")[1]
	dbhandle.use_db(db)

@parse("CREATE")
def CreateParse(dbhandle,sql):
	sql = rmNoUseChar(sql)
	sql = upperKetWord(sql)
	pattern = "^CREATE TABLE (.*?) \((.*?) \);"
	pattern = re.compile(pattern,re.S)
	value = re.findall(pattern,sql)
	if value != None:
		tableinfo = value[0]
		tablename = tableinfo[0]
		tableattrs = tableinfo[1:][0]
		tableattrs = tableattrs.split(",")
		attrlist = []
		for attr in tableattrs:
			attr = attr.strip(" ")
			attr = attr.rstrip(" ")
			attr = attr.split(" ",2)
			attrlist.append(attr)
		rcformat = getFormat(*attrlist)
		rcformat = ["__format__",rcformat]
		attrlist.append(rcformat)
		dbhandle.create_table(tablename,*attrlist)
		# 	attrdic[attrname] = attrvalue
		# attrdic["__format__"] = getFormat(**attrdic)
		# print attrdic
		# dbhandle.create_table(tablename,**attrdic)
	else:
		raise SYNTAXERROR

@parse("INSERT")
def InsertParse(dbhandle,sql):
	pass

@parse("DELETE")
def DeleteParse(dbhandle,sql):
	pass


@parse("UPDATE")
def UpdateParse(dbhandle,sql):
	pass

@parse("GRANT")
def GrantParse(dbhandle,sql):
	pass


if __name__ == '__main__':
	creatsql = """
	                  CREATE TABLE STUDENT
	(SNO CHAR(9) PRIMARY KEY               ,
	SNAME CHAR(20) UNIQUE,
	SSEX CHAR(2),
	SAGE INT,
	SDEPT CHAR(20)
	);"""

	helpsql = """
	help table tablename"""
	print CreateParse(None, creatsql)
