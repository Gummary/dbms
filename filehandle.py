import os,struct


class RCFileInfo:

	def __init__(self,rcsize= 0,rcnums = 0,fm = None):
		self.rcsize_ = rcsize
		self.rcnums_ = rcnums
		self.format_ = fm


	def pack_info(self):
		fm = '2i%ds'%len(self.format_)
		byte = struct.pack(fm,self.rcsize_,self.rcnums_,self.format_)
		return byte

	def unpack_info(self,byte):
		fm = '2i%ds'% (len(byte) - 8)
		self.rcsize_,self.rcnums_,self.format_ = struct.unpack(fm,byte)

	def show(self):
		return [self.rcsize_,self.rcnums_,self.format_]

	

class FileHandle:

	def __init__(self,filename,rcsize):
		self.filename = filename
		self.isopen = False
		self.rcsize = rcsize

	def write_line(self,data,num):
		if not self.isopen:
			raise Exception("File not open")

		self.__move_to_rc__(num)
		data += '\n'
		self.file.write(data)
		self.file.flush()

	def read_line(self,num):
		if not self.isopen:
			raise Exception("File not open")
		
		self.__move_to_rc__(num)
		data = self.file.readline().rstrip('\n')
		if len(data) == 0:
			return None
		else:
			return data


	def close_file(self):
		if self.isopen:
			self.file.flush()
			self.file.close()
			self.isopen = False
		else:
			raise Exception("File is not open")

	def open_file(self):
		if not os.path.isfile(self.filename):
			raise Exception("File not exist")


		if not self.isopen:
			try:
				self.file = open(self.filename, 'rb+')
				self.isopen = True
				byte = self.file.readline().rstrip('\n')
				fileinfo = RCFileInfo()
				fileinfo.unpack_info(byte)
				return fileinfo
			except Exception, e:
				raise e
		else:
			raise Exception("%s is already opened."%self.filename)




	def create_file(self,fileinfo):
		if os.path.isfile(self.filename):
			raise Exception("File already exists")

		try:
			file = open(self.filename,'w')
			if isinstance(fileinfo, RCFileInfo):
				byte = fileinfo.pack_info()
				byte+='\n'
				file.write(byte)
				file.flush()
				file.close()
			else:
				raise Exception("FileInfo must be RCFileInfo class")
		except Exception, e:
			raise e
		
		

	def remove_file(self):
		os.remove(self.filename)

	def get_filehdr(self):
		if not self.isopen:
			raise Exception("File not Open")

		self.__move_to_filehead__()
		fileinfo = RCFileInfo()
		fileinfo.unpack_info(self.file.readline().rstrip('\n'))
		return fileinfo

	def write_filehdr(self,fileinfo):
		if not self.isopen:
			raise Exception("File not Open")

		if not isinstance(fileinfo, RCFileInfo):
			raise Exception("fileinfo must be RCFileInfo class")
		self.__move_to_filehead__()
		byte = fileinfo.pack_info()
		byte += '\n'
		self.file.write(byte)
		self.file.flush()

	def __move_to_filehead__(self):
		self.file.seek(0)

	def __move_to_rc__(self,num):
		num+=1
		self.file.seek(9+(self.rcsize+1)*(num-1))