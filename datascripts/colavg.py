#!/usr/bin/python

import sys
import re

def sumline(sameline, filecount):
	#print sameline
	sum = 0
	i = 0
	line = ""

	for i in range(0, filecount):
		sum = sum + int(sameline[i].split()[0])

	line = str(sum/filecount)
	i = 0
	sum = 0
	x = 0

	for i in range(1, len(sameline[0].split())):
		#print "i" + str(i) + sameline[0]
		for x in range(0, len(sameline)):
			#print "x" + str(x)
			sum = sum + float(sameline[x].split()[i])
			#print sameline[x].split()[i]
			#print sameline[x].split()[i]
		
		line = line + " " + str(sum/filecount)
		sum = 0

	print line


def main():
	
	files = []
	datalines = []

	files = map((lambda x: open(x)), sys.argv[1:])

	datalines = map((lambda x: x.readlines()), files)
	
	numlines = map((lambda x: map((lambda y: y.strip()), x)), datalines)
	
	datalines = map((lambda x: filter((lambda y: y[0] != "#"), x)), numlines)

	linecount = len(datalines[0])
	filecount = len(files)

	sameline = []
	i = 0
	for i in range(0, linecount):
		sameline = []
		for file_line in range(0, filecount):
			sameline.append(datalines[file_line][i])

		sumline(sameline, filecount)



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "No filename given."
		print "USAGE: colavg <file1> <file2> ... <fileN>"
		sys.exit(0);

	main()

