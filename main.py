from user import User
from parseSql import ParseSql

if __name__ == "__main__":
    u = User()
    permit = u.get_user_permissin()
    p = new ParseSql()
    p.set_user_permit(u,permit)
