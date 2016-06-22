from filehandle import FileHandle,FileInfo
from error import RC_Error
import struct,enum

class RecordHandle():
	"""docstring for RecordHandle"""
	def __init__(self,filename,rcsize,rcformat):
		rcformat = 'i'+rcformat
		rcsize +=4
		self.fileinfo = FileInfo(rcsize, 0, rcformat)
		self.filename = filename

	def create_file(self):
		self.fh = FileHandle(self.filename, self.fileinfo.rcsize_)
		try:
			self.fh.create_file(self.fileinfo)
		except Exception, e:
			raise e

	def desrory_file(self):
		self.fh.remove_file()

	def open_file(self):
		try:
			self.fileinfo_ = self.fh.open_file()
		except Exception, e:
			raise e
		
	def close_file(self):
		try:
			self.fh.close_file()
		except Exception, e:
			raise e

	def insert_record(self,rcdata):
		num = self.__get_free_slot__()
		if isinstance(rcdata, list):
			data = struct.pack(self.fileinfo_.format_,1,*rcdata)
			self.fh.write_line(data,num)
			return num
		else:
			raise Exception("rcdata must be list")
		
	def delete_record(self,num):
		try:
			data = struct.pack('i',0)
			self.__update_record__(data, num)
		except Exception, e:
			raise e	

	def update_record(self,rcdata,num):
		if isinstance(rcdata, list):
			try:
				data = struct.pack(self.fileinfo_.format_,1,*rcdata)
				self.__update_record__(data, num)
			except Exception, e:
				raise e		
		else:
			raise Exception("record must be list")

	def __update_record__(self,rcdata,num):
		index = 1
		while True:
			data = self.fh.read_line(index)
			if data == None:
				print index
				raise Exception("Update Rc:num is too big")
			
			num-=1
			if num == 0:
				if len(data) == 4:
					raise Exception("RC is deleted")
				self.fh.write_line(rcdata,index)
				break
			index += 1

	def get_record(self,num):
		index = 1
		while True:
			data = self.fh.read_line(index)
			if data == None:
				return RC_Error.FILE_EOF
			
			num-=1
			if num == 0:
				if len(data) == 4:
					return RC_Error.EMPTY_RC
				d = struct.unpack(self.fileinfo_.format_,data)[1:]
				return d
			index += 1


	def __get_free_slot__(self):
		index = 1
		data = self.fh.read_line(index)
		while data != None:
			if len(data) == 4:
				break
			else:
				index += 1
				data = self.fh.read_line(index)

		return index

	def show_all_record(self):
		index = 1
		data = self.get_record(index)
		while data != RC_Error.FILE_EOF:
			if data != RC_Error.EMPTY_RC:
				print data

			index +=1
			data = self.get_record(index)


