import pypyodbc

dbname = r'C:\Users\atole\Desktop\DB.accdb'
constr = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={0};".format(dbname)

dbconn = pypyodbc.connect(constr)

cur = dbconn.cursor()
cur.execute("""CREATE TABLE Table1 (
                 ID autoincrement,
                 Col1 varchar(50),
                 Col2 double,
                 Col3 datetime);""")
dbconn.commit()
cur.close()
dbconn.close()
