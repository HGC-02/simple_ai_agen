import sqlite3

def catalog(database):
    d=sqlite3.connect(database)
    d_curr=d.cursor()
    d_curr.execute("CREATE TABLE catalog (id INTEGER PRIMARY KEY,time VARCHAR(13),title VARCHAR(225),tag);")
    d.commit()
    d.close()
def file_path(database):
    d=sqlite3.connect(database)
    d_curr=d.cursor()
    d_curr.execute("")#name file path (id PK ,title FK ,path(path return to ai))
    d.commit()
    d.close

