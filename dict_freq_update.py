# 20170313

import leveldb
import re

path = 'foo/'
schema = 'bar'

db_temp = leveldb.LevelDB(path + 'data_temp')
for couple in db_temp.RangeIter():
	db_temp.Delete(couple[0])

db_prime = leveldb.LevelDB(path + schema + '.userdb')
for couple in db_prime.RangeIter():
	if ord(couple[0][0]) < 11:
		continue
	key = re.sub('(.+) \t(.+)', '\\2\t\\1', couple[0])
	freq = re.sub('c=([-\d]+) .+', '\\1', couple[1])
	if int(freq) < 0:
		continue
	db_temp.Put(key, freq)

fin = open(schema + '.dict.yaml', 'r')
lines = fin.readlines()
fin.close()
start_pos = lines.index('...\n')

for line in lines[start_pos+1:]:
	line = line.replace('\n', '')
	cells = line.split('\t')
	num_cells = len(cells)
	if num_cells < 2:
		continue
	key = cells[0] + '\t' + cells[1]
	freq = (cells[2] if num_cells == 3 else '0')
	freq2 = db_temp.Get(key, default = '0')
	db_temp.Put(key, str(int(freq) + int(freq2)))

fout = open(schema + '.dict2.yaml', 'w')
for line in lines[:start_pos+1]:
	fout.write(line);
for couple in db_temp.RangeIter():
	print >> fout, couple[0] + '\t' + couple[1]
fout.close()


