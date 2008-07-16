#!/usr/bin/python



import os
import sys
import re



def create_line_tokens(line):

	#try to remove multiple whitespaces
	nospc_line = re.sub("\ +", " ", line.strip())
	tokens = nospc_line.split(" ")
	return tokens


def is_sample_line(line):
	sample_line_re = re.compile("^[0-9]")
	return sample_line_re.match(line)

def create_events_list_from_file(evfname):
	global event_column
	eventslist = []

	#lines containing samples in oprofile output start with
	#numbers
	nosymbol_re = re.compile("^\(")
	evfile = open(evfname, "r")

	for line in evfile:
		if is_sample_line(line):
			tokens = create_line_tokens(line)
			if not nosymbol_re.match(tokens[event_column]):
				eventslist.append(tokens[event_column])

	evfile.close()
	return eventslist



def create_events_list(datfnames):
	full_events_list = []
	for dfname in datfnames:
		events_list = create_events_list_from_file(dfname)
		full_events_list = full_events_list + events_list

	uniq_events_list = list(set(full_events_list))
	uniq_events_list.sort()
	return uniq_events_list


def get_event_line_from_file(event, dfname):
	global event_column
	dfile = open(dfname, "r")
	for line in dfile:
		if is_sample_line(line):
			tokens = create_line_tokens(line)
			if tokens[event_column] == event:
				return line
	
	dfile.close()
	return None 


def extract_event_data_rows(event, dfnames):
	event_lines = []

	for dfname in dfnames:
		evline = get_event_line_from_file(event, dfname)
		if evline is not None:
			event_lines.append(evline)

	return event_lines


def create_event_data_row(event, evlines):
	global data_column
	evrow = event

	for row in evlines:
		tokens = create_line_tokens(row)
		evrow = evrow + " " + tokens[data_column]

	return evrow

def main(filenames):
	datfiles = filenames
	#print filenames
	evlist = create_events_list(datfiles)
	#for each event, go through the data file and extract
	#its line which contains the share of CPU usage.
	for event in evlist:
		#print event
		event_lines = extract_event_data_rows(event, datfiles)
		datarow = create_event_data_row(event, event_lines)
		print datarow


if __name__ == "__main__":
	global event_column
	global data_column
	global default_event_column
	global default_data_column

	default_event_column = 3
	default_data_column = 1
	
	lastarg = 1
	tmp = 1

	if len(sys.argv) <= 1:
		print "Need list of files containing oprofile output."
		print "Usage:  procdata --eventcolumn <coln> --datacolumn <coln>"
		sys.exit(-1)
		
	if "--eventcolumn" in sys.argv:
		tmp = sys.argv.index("--eventcolumn") + 1
		event_column = int(sys.argv[tmp])
	else:
		event_column = default_event_column
	
	lastarg = tmp
	if "--datacolumn" in sys.argv:
		tmp = sys.argv.index("--datacolumn") + 1
		data_column = int(sys.argv[tmp])
	else:
		data_column = default_data_column
	
	if tmp > lastarg:
		lastarg = tmp

	lastarg = lastarg + 1
	#print str(event_column) + " " + str(data_column)
	main(sys.argv[lastarg:])

