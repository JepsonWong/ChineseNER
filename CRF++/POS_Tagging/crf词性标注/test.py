#encoding:utf-8

fiobj = open('./people-daily.txt','r')
arr = fiobj.readlines()

line = arr[5];
print line
line = line.strip('\t\n\t ')
print line
words = line.split(' ')
print words

for word in words[1:]:
	word = word.strip('\t ')
	print len(word)
