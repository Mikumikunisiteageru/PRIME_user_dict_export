# 20170218
import leveldb
db = leveldb.LevelDB("your_path/your_ime_name.userdb")
f = open("your_ime_name.txt", "w")
for element in db.RangeIter():
	print >> f, element
f.close()

