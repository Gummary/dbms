class EOF(Exception):
	def __init__(self,value = None):
		self.value = value

class EMPTY_RC(Exception):
	def __init__(self,value = None):
		self.value = value

class NODBSELE(Exception):
	def __str__(self):
		return "No database selected"

class NOSUCHDB(Exception):
	def __init__(self,dbname):
		self.name = dbname

	def __str__(self):
		return "There is no database named %s" % self.name

class DBEXISTS(Exception):
	def __init__(self,dbname):
		self.name = dbname

	def __str__(self):
		return "DataBase %s is already exists" % self.dbname

class TABLEEXISTS(Exception):
	def __init__(self,tablename):
		self.name = tablename
	def __str__(self):
		return "Table %s is already exists" % self.name
class TABLENOTEXISTS(Exception):
	def __init__(self,tablename):
		self.name = tablename

	def __str__(self):
		return "There is no table named %s" %self.name

class SYNTAXERROR(Exception):
	def __init__(self):
		pass
	def __str__(self):
		return "Syntax error"
class TYPEERROR(Exception):
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return "Type %s not exist"%self.name

class ATTRNOTEXISTS(Exception):
	def __init__(self,name):
		self.name = name
	def __str__(self):
		return "Attributes %s not exists"%self.name


class ExceedLimit(Exception):
	def __init__(self,name):
		self.name = name
	def __str__(self):
		return "The length of %s is exceed limit"%self.name

class NONEVALUE(Exception):
	def __init__(self,name):
		self.name = name
	def __str__(self):
		return "%s must not be None"%self.name

class UNAUTHORIZED(Exception):
	def __init__(self,name):
		self.name = name
	def __str__(self):
		return "The %s in unauthorized"%self.name
