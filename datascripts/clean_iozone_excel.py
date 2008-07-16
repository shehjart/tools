#!/usr/bin/python

import sys
import re
import string



def get_tput_lines(file, token):

	tputre = re.compile("^\"Throughput")
	complete_re = re.compile("^iozone test complete")
	newline_re = re.compile("^\n")
	rec_re = re.compile("^\"Record size")
	outp_re = re.compile("^\"Output is")
	
	tputlines = ""
	newlines = 0
	prev_newline = None
	
	for line in file:
		if tputre.match(line):
			break
	
		if complete_re.match(line):
			return tputlines

	for line in file:

		if newline_re.match(line):
			if prev_newline is True:
				break
			else:
				prev_newline = True
				continue
		else:
			prev_newline = False

		if rec_re.match(line) or outp_re.match(line):
			continue
		
		line = line.replace("\"","")
		line = line.replace("Initial write", "Write")
		line = line.replace("Random write", "RandomWrite")
		line = line.replace("Random read", "RandomRead")
		linearr = line.split()
		line2 = string.join(linearr)

		if len(line2) > 0:
			tputlines = tputlines + "\n" + str(token) + line2.strip()

	return tputlines


def get_cpu_lines(file, token):

	cpure = re.compile("^\"CPU utilization")
	complete_re = re.compile("^iozone test complete")
	newline_re = re.compile("^\n")
	rec_re = re.compile("^\"Record size")
	outp_re = re.compile("^\"Output is")
	
	cpulines = ""
	newlines = 0
	prev_newline = None
	
	for line in file:
		if cpure.match(line):
			break
	
		if complete_re.match(line):
			return tputlines

	for line in file:

		if newline_re.match(line):
			if prev_newline is True:
				break
			else:
				prev_newline = True
				continue
		else:
			prev_newline = False

		if rec_re.match(line) or outp_re.match(line):
			continue
		
		line = line.replace("\"","")
		line = line.replace("Initial write", "Write")
		linearr = line.split()
		line2 = string.join(linearr)

		if len(line2) > 0:
			cpulines = cpulines + "\n" + str(token) + line2.strip()

	return cpulines


	

def clean_iozone_excel(file, tput_file, cpu_file, token):

	cpure = re.compile("^\"CPU")
	
	if token is not None:
		tstr = str(token)
	else:
		tstr = ""
	
	if tput_file is not None:
		tputlines = get_tput_lines(file, tstr)
		if tput_file == "-":
			tfile = sys.stdout
		else:
			tfile = open(tput_file, "w")
		
		tfile.write(tputlines)

		if tput_file <> "-":
			tfile.close()


	if cpu_file is not None:
		cpulines = get_cpu_lines(file, tstr)
		if cpu_file == "-":
			cpufile = sys.stdout
		else:
			cpufile = open(cpu_file, "w")

		cpufile.write(cpulines)

		if cpu_file <> "-":
			cpufile.close()

def main():

	tfile = None
	cfile = None
	token = None

	if sys.argv[1] == "-":
		f = sys.stdin
	else:
		f = open(sys.argv[1], "r")

	if "-t" in sys.argv:
		tfile = sys.argv[sys.argv.index("-t") + 1]
	
	if "-c" in sys.argv:
		cfile = sys.argv[sys.argv.index("-c") + 1]

	if "--token" in sys.argv:
		token = sys.argv[sys.argv.index("--token") + 1]
	
	clean_iozone_excel(f, tfile, cfile, token)

def usage():

	print "USAGE: clean_iozone_excel <input_file> <OPTIONS>"
	print "Options:"
	print "\t\t-t <tputfile>"
	print "\t\t\tThroughput data output file."
	print "\n\t\t-c <cpufile>"
	print "\t\t\tCPU Data output file."
	print "\t\t--token <token>"
	print "\t\t\tToken to prepend to column headers."
	sys.exit(0)


if __name__ == "__main__":
	if len(sys.argv) < 4:
		usage()

	main()
