from parseSql import parse
from error import SYNTAXERROR,TABLENOTEXISTS,TYPEERROR
import re

oneKeywords = ["SELECT","FROM","WHERE",
	"DESC","ASC",
	"DATE","DAY","INT","CHAR","VARCHAR","DECIMAL",
	"SUM","AVG","COUNT","AS","TOP","AND","OR"]
twoKeywords = ["GROUP BY","ORDER BY"]
stmtTag = ["SELECT","FROM","WHERE","GROUP BY","ORDER BY",";"]

def rmListSpace(li):
    while "" in li:
        li.remove("")
    return li
def nextStmtTag(sql,currentTag):
    index = sql.find(currentTag,0)
    for tag in stmtTag:
        if sql.find(tag,index+len(currentTag)) != -1:
            return tag
def rmStrSpace(string):
    li = string.split(" ")
    li = rmListSpace(li)
    result = ''
    for word in li:
        result += word+" "
    return result[0:-1]

def rmNoUseChar(sql):
    sql = sql.replace(";"," ;")
    while sql.find("'") != -1:
        sql = sql.replace("'","")
    while sql.find('"') != -1:
        sql = sql.replace('"','')
    while sql.find('\t') != -1:
        sql = sql.replace("\t"," ")
    while sql.find('\n') != -1:
        sql = sql.replace("\n"," ")
    statements = sql.split(" ")
    while "" in statements:
        statements.remove("")
    sql=""
    for stmt in statements:
        sql += stmt+ " "
    return sql[0:-1]

def upperKeywords(sql):
	for key in twoKeywords:
	    lKey = key.lower()
	    if lKey in sql:
	        sql = sql.replace(lKey,key)
	stmts = sql.split(" ")
	for key in oneKeywords:
	    lKey = key.lower()
	    for i in range(len(stmts)):
			stmt = stmts[i]
			if stmt == lKey or (lKey+",") == stmt or(lKey in stmt and "(" in stmt):
				stmts[i] = stmt.replace(lKey,key)
	sql = ""
	for stmt in stmts:
	    sql += stmt+ " "
	return sql

def parseSelect(sql):
	selectAttr = []
	reg = "SELECT (.+) FROM"
	select = re.compile(reg).findall(sql)[0]
	selectList = select.split(",")
	for eachAttr in selectList:
	    attrAggre = eachAttr.split(" ")
	    attrAggre = rmListSpace(attrAggre)
	    if len(attrAggre) <= 2:
	        selectAttr.append([attrAggre[0].upper(),None,None])
	    elif "(" in attrAggre[0]:
	        reg = "^(.+)\("
	        aggre = re.compile(reg).findall(attrAggre[0])[0]
	        reg = "\((.+)\)"
	        attrName = re.compile(reg).findall(attrAggre[0])[0]
	        selectAttr.append([attrName.upper(),aggre,attrAggre[2]])
	    elif "TOP" in attrAggre[0]:
	        attrs = attrAggre[2].split(",")
	        attrs = rmListSpace(attrs)
	        for each in attrs:
	            selectAttr.append([each.upper(),attrAggre[0],attrAggre[1]])

	    else:
	        selectAttr.append([attrAggre[0].upper(),None,attrAggre[2]])
	return selectAttr

def parseFrom(sql):
    nextKey = nextStmtTag(sql,"FROM")
    reg = "FROM (.+) "+nextKey
    froms = re.compile(reg).findall(sql)[0]
    table = froms.split(",")
    table = rmListSpace(table)
    for i in range(len(table)):
        table[i] = table[i].upper().replace(" ","")
    return table

def parseWhere(sql):
    conditions = []
    if "WHERE " not in sql:
        return None
    nextKey = nextStmtTag(sql,"WHERE")
    reg = "WHERE (.+) "+nextKey
    where = re.compile(reg).findall(sql)[0]
    whereStmt = where.split(" AND ")
    for stmt in whereStmt:
        if "<=" in stmt:
            compare = "<="
        elif ">=" in stmt:
            compare = ">="
        elif "=" in stmt:
            compare = "="
        elif "<" in stmt:
            compare = "<"
        elif ">" in stmt:
            compare = ">"
        reg = "^(.+)\s*"+compare
        attr = re.compile(reg).findall(stmt)[0]
        attr = rmStrSpace(attr).upper()
        reg = compare+"\s*(.+)$"
        value = re.compile(reg).findall(stmt)[0]
        value = rmStrSpace(value)
        conditions.append([attr,compare,value])
    return conditions
def parseGroup(sql):
    groupby = []
    if "GROUP BY" not in sql:
        return None
    nextKey = nextStmtTag(sql,"GROUP BY")
    reg = "GROUP BY (.+) "+nextKey
    group = re.compile(reg).findall(sql)[0]
    groupStmt = group.split(",")
    groupStmt = rmListSpace(groupStmt)
    for each in groupStmt:
        groupby.append(rmStrSpace(each).upper())
    return groupby

def parseOrder(sql):
    orderby = []
    if "ORDER BY" not in sql:
        return None
    reg = "ORDER BY (.+);"
    order = re.compile(reg).findall(sql)[0]
    order = rmStrSpace(order)
    orders = order.split(",")
    for each in orders:
        each = rmStrSpace(each)
        ascDesc = each.split(" ")
        ascDesc = rmListSpace(ascDesc)
        if len(ascDesc) == 1:
            orderby.append([ascDesc[0].upper(),"ASC"])
        else:
            orderby.append([ascDesc[0].upper(),ascDesc[1].upper()])
    return orderby

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
	sql = rmNoUseChar(sql)
	sql = upperKeywords(sql)
	sqlDic = {}
	sqlDic["SELECT"]= parseSelect(sql)
	sqlDic["FROM"]=  parseFrom(sql)
	sqlDic["WHERE"]= parseWhere(sql)
	sqlDic["GROUP"]= parseGroup(sql)
	sqlDic["ORDER"]= parseOrder(sql)
	print sqlDic

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
	sql = rmNoUseChar(sql)
	sql = upperKetWord(sql)
	pattern1 = "INSERT INTO (\w+)\((.*?)\) VALUES\((.*?)\)"
	pattern1 = re.compile(pattern1,re.S)
	pattern2 = "INSERT INTO (\w+) VALUES\((.*?)\)"
	pattern2 = re.compile(pattern2,re.S)
	if re.match(pattern1,sql) != None:
		value = re.findall(pattern1,sql)[0]
		tablename = value[0]
		attrsname = value[1].split(",")
		attrsvalue = value[2].split(",")
		attrs = {}
		for i in range(0,len(attrsname)):
			attrs[attrsname[i]] = attrsvalue[i]
		# print attrs
		dbhandle.insert_record(tablename,attrs)

	elif re.match(pattern2,sql) != None:
		value = re.findall(pattern2,sql)[0]
		tablename = value[0]
		attrsvalue = value[1].split(",")
		# print tablename
		# print attrsvalue
		dbhandle.insert_record(tablename,attrsvalue)
	else:
		raise SYNTAXERROR

@parse("DELETE")
def DeleteParse(dbhandle,sql):
	pass


@parse("UPDATE")
def UpdateParse(dbhandle,sql):
	pass

@parse("GRANT")
def GrantParse(dbhandle,sql):
	sql = rmNoUseChar(sql)
	sql = upperKetWord(sql)
	# print sql
	pattern = "GRANT (\w+) ON TABLE (\w+) TO (.*?)$"
	re.compile(pattern,re.S)
	result = re.findall(pattern, sql)[0]
	perlist = result[0].split(",")
	while "" in perlist :
		perlist.remove("")
	tablelist = result[1].split(" ")
	while "" in tablelist:
		tablelist.remove("")
	userlist = result[2].split(",")
	while "" in userlist:
		userlist.remove("")
	perdic = {}
	for per in perlist:
		perdic[per] = tablelist
	dbhandle.update_user(userlist,perdic)

@parse("REVOKE")
def RevokeParse(dbhandle,sql):
	pass


if __name__ == '__main__':
	# creatsql = """
	#                   CREATE TABLE STUDENT
	# (SNO CHAR(9) PRIMARY KEY               ,
	# SNAME CHAR(20) UNIQUE,
	# SSEX CHAR(2),
	# SAGE INT,
	# SDEPT CHAR(20)
	# );"""
	#
	# helpsql = """
	# help table tablename"""
	# print CreateParse(None, creatsql)
	# """
	# INSERT INTO (.*?)\((.*?)\) VALUES\((.*?)\)
	# """
	# insertsql1 = """
	# INSERT
	# INTO Student(snao,Sname,Ssex,Sdept,Sage)
	# VALUES('20151218','CHENDONG',"MAN","IS",18)
	# """
	# insertsql2 = """
	# INSERT
	# INTO Student
	# VALUES('20151218','CHENDONG',"MAN","IS",18)
	# """
	# insertsql3 = """
	# INSERT
	# INTO Student(Sdept,Sage)
	# VALUES("IS",18)
	# """
	# print "1"
	# print InsertParse(None,insertsql1)
	# print "2"
	# print InsertParse(None,insertsql2)
	# print "3"
	# print InsertParse(None,insertsql3)
	# gsql1 = """
	# GRANT SELECT
	# ON TABLE STUDENT
	#  TO U1,U2
	#  """
	# GrantParse(None,gsql1)
	selectsql ="""select  * from STUDENT where SNO= '2015014010';"""
	SeltctParse(None,selectsql)
