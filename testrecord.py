from record import RecordHandle
from random import Random
from database import DataBase
import threading,struct

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def random_num(randomlength = 10):
	str = ''
	chars = '0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str+=chars[random.randint(0, length)]
	return str

ctx = threading.local()
# 10s Name
# 5s  Class
# 10s Sno
# i   age
ctx.format = '10s5s10si'
ctx.filename = 'Student_db'
ctx.db = None


def TestOpenAndClose():
	print '======StartTestingOpenandCloseFunc======'
	rh = RecordHandle(ctx.filename,struct.calcsize(ctx.format), ctx.format)
	try:
		rh.create_file()
		rh.open_file()
		print rh.fileinfo_.show()
		rh.close_file()
	except Exception, e:
		print e
	print '===================End=================='

def TestRecordChanged():
	print "=====StartTestingInsertFunc======"
	rh = RecordHandle(ctx.filename,struct.calcsize(ctx.format), ctx.format)
	try:
		rh.create_file()
		rh.open_file()
	except Exception  ,e:
			rh.open_file()
	i = 0
	for i in range(0,10):
		rcdata = [random_str(10),random_str(5),random_num(10),17]
		rh.insert_record(rcdata)
	rh.show_all_record()
	print '===================End=================='
	print "=====StartTestingDeleteFunc======"
	for i in range(1,1000):
		rh.delete_record(i)
	rh.show_all_record()
	rh.close_file()
	print '===================End=================='


def TestInsert():
	rh = RecordHandle(ctx.filename,struct.calcsize(ctx.format), ctx.format)
	try:
		rh.create_file()
		rh.open_file()
	except Exception  ,e:
		rh.open_file()
	i = 1
	for i in range(0,10):
		rcdata = [random_str(10),random_str(5),random_num(10),17]
		rh.insert_record(rcdata)
	rh.show_all_record()
	rh.close_file()

def TestDele():
	rh = RecordHandle(ctx.filename,struct.calcsize(ctx.format), ctx.format)
	try:
		rh.create_file()
		rh.open_file()
	except Exception  ,e:
			rh.open_file()
	rh.delete_record(1)
	rh.delete_record(3)
	rh.delete_record(4)
	rh.delete_record(5)
	rh.show_all_record()
	rh.close_file()

def TestUpdateRc():
	rcdata = [random_str(10),random_str(5),random_num(10),17]
	rh = RecordHandle(ctx.filename,struct.calcsize(ctx.format), ctx.format)
	try:
		rh.create_file()
		rh.open_file()
	except Exception  ,e:
		rh.open_file()
	rh.update_record(rcdata, 5)
	rh.show_all_record()
	rh.close_file()


def TestCreateDB():
	ctx.db = DataBase()
	i = 0
	dbname = random_str(5)
	ctx.db.creat_db(dbname)
	ctx.db.use_db(dbname)
	value = "CHAR(5)"
	for i in range(0,10):
		tablename = random_str(3)
		atrdic = {}
		for i in range(0,10):
			attrname = random_str(4)
			value = "CHAR(%s)"%random_num(1)
			atrdic[attrname] = value
		ctx.db.create_table(tablename,**atrdic)
	ctx.db.quitdb(dbname)
	ctx.db.show_alldb()
	ctx.db.use_db(dbname)
	ctx.db.show_all_tables()
	ctx.db.quitdb(dbname)
	ctx.db.quit()





if __name__ == '__main__':
	# try:
	# 	TestInsert()
	# except Exception, e:
	# 	print e

	# print "============"
	# try:
	# 	TestDele()
	# except Exception, e:
	# 	print e
	TestCreateDB()
