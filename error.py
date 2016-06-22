from enum import Enum,unique

@unique
class RC_Error(Enum):
	FILE_EOF = 1
	EMPTY_RC = 2