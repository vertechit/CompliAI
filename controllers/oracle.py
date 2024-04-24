import oracledb
import getpass

oracledb.init_oracle_client()

userpwd = getpass.getpass("Enter password: ")

connection = oracledb.connect(user="vch_eso", password=userpwd,dsn="10.10.2.251/comvdev01.comvdev.comvertvcn.oraclevcn.com")

cursor = connection.cursor()
cursor.execute("select * from cin_empr_usu where gremp_id = :en_gremp_id", en_gremp_id=1)
print(cursor.description)
print('------------')
print(cursor.fetchall())

cursor.close()
connection.close()