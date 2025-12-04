# Sử dụng pymysql thay cho mysqlclient nếu cần
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
