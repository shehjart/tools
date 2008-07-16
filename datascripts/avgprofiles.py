#!/usr/bin/python


import sys
import re


all_lines = []
processed_events = []

def get_all_lines(event):
	global all_lines
	event_lines = []

	event_re = re.compile("^" + event)
	for line in all_lines:
		if event_re.match(line):
			event_lines.append(line)

	return event_lines

def get_max_cols(event_lines):

	max_cols = 0
	for line in event_lines:
		cols_in_line = len(line.split(" ")) - 1
		if cols_in_line > max_cols:
			max_cols = cols_in_line

	return max_cols



def get_averaged_col(event_lines, colnum):

	total = 0
	count = 0

	for line in event_lines:
		tokens = line.split(" ")
		if len(tokens) > colnum:
			total = total + float(tokens[colnum])
			count = count + 1
	
	return total/float(count)



def get_averaged_event_line(event, event_lines):

	value = 0
	average_line = event
	
	max_cols = get_max_cols(event_lines)
	for col in range(1, max_cols + 1):
		col_avg = get_averaged_col(event_lines, col)
		average_line = average_line + " " + str(col_avg)

	return average_line

def main(args):
	global all_lines
	global processed_events

	for line in sys.stdin:
		line = line.strip()
		all_lines.append(line)

	for line in all_lines:
		token = line.split(" ")
		if not token[0] in processed_events:
			event_lines = get_all_lines(token[0])
			processed_events.append(token[0])
			aline = get_averaged_event_line(token[0], event_lines)
			print aline

if __name__ == "__main__":
	main(sys.argv)
