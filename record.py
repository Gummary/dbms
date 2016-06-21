from filehandle import FileHandle,FileInfo
import struct

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
		num-=1
		data = self.fh.read_line(index)
		while data != None and num != 0:
			if len(data) != 4:
				num -= 1
			data = self.fh.read_line(index)
			index += 1
		if data != None and len(data) != 4:
			self.fh.write_line(rcdata,index)
		else:
			raise Exception("Record not exists")

	def get_record(self,num):
		data = self.fh.read_line(num)
		data = struct.unpack(self.fileinfo_.format_)[1:]
		return data

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
		data = self.fh.read_line(index)
		while data != None:
			if len(data) == 4:
				index += 1
				data = self.fh.read_line(index)
				continue
			d = struct.unpack(self.fileinfo_.format_,data)[1:]
			print d
			index += 1
			data = self.fh.read_line(index)


