from error import SYNTAXERROR,UNAUTHORIZED
from database import DataBase

oneKeywords = ["SELECT","FROM","WHERE",
	"DESC","ASC",
	"DATE","DAY","INT","CHAR","VARCHAR","DECIMAL",
	"SUM","AVG","COUNT","AS","TOP","AND","OR","HELP","TABLE","VALUES"]
twoKeywords = ["GROUP BY","ORDER BY","HELP DATABASE","INSERT INTO","CREATE TABLE"]
stmtTag = ["SELECT","FROM","WHERE","GROUP BY","ORDER BY",";"]


def rmNoUseChar(sql):
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

def upperKetWord(sql):
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

def parse(sql):
	def wrapper(func):
		func.__sql__= sql
		return func
	return wrapper


class ParseSql():
	def __init__(self):
		self.parsefunc = {}
		self.dbhandle = DataBase()
		self.userpermit = []
		import parsefunc
		self.load_func(parsefunc)

	def load_func(self,mod):
		m = dir(mod)
		for func in m:
			f = getattr(mod, func)
			if callable(f) and hasattr(f, "__sql__"):
				name = getattr(f, "__sql__").upper()
				self.parsefunc[name] = f

	def parse_sql(self,sql):
		sql = rmNoUseChar(sql)
		sql = upperKetWord(sql)
		if "quit" in sql:
			import sys
			sys.exit(0)
		funcname = sql.split(" ")[0].upper()
		if self.parsefunc.has_key(funcname):
			if funcname not in self.userpermit:
				raise UNAUTHORIZED(funcname)
			self.parsefunc[funcname](self.dbhandle,sql)
		else:
			raise SYNTAXERROR


	def clean_sql(self,sql):
		sql.rstrip()
		sql.strip()
		return sql

	def set_user_permit(self,user,permit):
		self.user = user
		self.userpermit = permit

	def update_userpermission(self,users,permission):
		for per in permission:
			tlist = permission[per]
			for table in tlist:
				if not self.dbhandle.has_table(table):
					print "%s not exist"%table
					tlist.remove(table)
			permission[per] = tlist
		self.user.update_user(user,permission)

	def __get_user_input__():
		while True:
			sql = raw_input()
			self.parse_sql(sql)


if __name__ == '__main__':
	parse = ParseSql()
	# hdbsql = "help database"
	# udbsql = "use gRAkx"
	# htbsql = "help table STUDENT"
	# ctbsql = """
	#                   CREATE TABLE STUDENT
	# (SNO CHAR(9) PRIMARY KEY               ,
	# SNAME CHAR(20) UNIQUE,
	# SSEX CHAR(3),
	# SAGE INT,
	# SDEPT CHAR(20)
	# );"""
	# insertsql1 = """
	# INSERT
	# INTO STUDENT(SNO,SNAME,SSEX,SAGE,SDEPT)
	# VALUES('20151218','CHENDONG',"MAN",18,"CS")
	# """
	# insertsql2 = """
	# INSERT
	# INTO STUDENT
	# VALUES('20151218','CHENDONG',"MAN",18,"CS")
	# """
	# insertsql3 = """
	# INSERT
	# INTO STUDENT(SNO,SDEPT,SAGE)
	# VALUES("20151218","IS",18)
	# """
	# # try:
	# parse.parse_sql(hdbsql)
	# parse.parse_sql(udbsql)
	# # parse.parse_sql(ctbsql)
	# parse.parse_sql(htbsql)
	# for i in range(0,1000):
	# 	parse.parse_sql(insertsql1)
	# 	parse.parse_sql(insertsql2)
	# 	parse.parse_sql(insertsql3)
	# except Exception as e:
	# 	print e
	try:
		quit = "quit"
		parse.parse_sql(quit)
	except Exception as e:
		print e
