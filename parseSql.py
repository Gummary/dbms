from error import SYNTAXERROR
from database import DataBase

oneKeywords = ["SELECT","FROM","WHERE",
	"DESC","ASC",
	"DATE","DAY","INT","CHAR","VARCHAR","DECIMAL",
	"SUM","AVG","COUNT","AS","TOP","AND","OR","HELP","TABLE"]
twoKeywords = ["GROUP BY","ORDER BY","HELP DATABASE","CREATE TABLE"]
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

	def load_func(self,mod):
		m = dir(mod)
		for func in m:
			f = getattr(mod, func)
			if callable(f) and hasattr(f, "__sql__"):
				name = getattr(f, "__sql__").upper()
				self.parsefunc[name] = f

	def parse_sql(self,sql):
		sql = self.clean_sql(sql)
		sql = rmNoUseChar(sql)
		sql = upperKetWord(sql)
		funcname = sql.split(" ")[0].upper()
		if self.parsefunc.has_key(funcname):
			self.parsefunc[funcname](self.dbhandle,sql)
		else :
			raise SYNTAXERROR


	def clean_sql(self,sql):
		sql.rstrip()
		sql.strip()
		return sql



if __name__ == '__main__':
	parse = ParseSql()
	import parsefunc
	parse.load_func(parsefunc)
	hdbsql = "help database"
	udbsql = "use gRAkx"
	htbsql = "help table STUDENT"
	ctbsql = """
	                  CREATE TABLE STUDENT
	(SNO CHAR(9) PRIMARY KEY               ,
	SNAME CHAR(20) UNIQUE,
	SSEX CHAR(2),
	SAGE INT,
	SDEPT CHAR(20)
	);"""
	try:
		parse.parse_sql(hdbsql)
		parse.parse_sql(udbsql)
		# parse.parse_sql(ctbsql)
		parse.parse_sql(htbsql)
	except Exception as e:
		print e
