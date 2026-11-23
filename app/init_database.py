import sqlite3

def catalog(database):
    d=sqlite3.connect(database)
    d_curr=d.cursor()
    d_curr.execute("CREATE TABLE catalog (id INTEGER PRIMARY KEY,time VARCHAR(13),title VARCHAR(225),tag);")
    d.commit()
    d_curr.execute("INSERT INTO catalog (time,title,tag)VALUES(NULL,'test','test');")
    d.commit()
    x=d_curr.execute("SELECT * FROM catalog")
    d.close()
    return x
def file_path(database):
    d=sqlite3.connect(database)
    d_curr=d.cursor()
    d_curr.execute("CREATE TABLE file_path (id INTEGER PRIMARY KEY,title VARCHAR(255),path)")#name file path (id PK ,title FK ,path(path return to ai))
    d.commit()
    d_curr.execute("INSERT INTO file_path (title,path)VALUES(NULL,'test')")
    d.commit()
    x=d_curr.execute("SELECT * FROM file_path")
    d.close
    return x

