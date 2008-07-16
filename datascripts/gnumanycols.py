#!/usr/bin/python

import sys

escape_for_eps = False
use_lw_token = False

def create_col_names(datafile):
	global escape_for_eps
	f = open(datafile, "r")
	line = f.readline()
	f.close()
	if escape_for_eps:
		line = line.replace("_", "-")

	return line.strip().replace("#","", 1).split(" ")


def printcols(cols):
	i = 0
	for col in cols:
		print str(i) + " " + col
		i = i + 1

def print_prelim_cmds(prelimfile):
	pcfile = open(prelimfile, "r")	
	for line in pcfile:
		print line

	pcfile.close()

	
def print_plot_cmd(datafile, columns, col_indices):
	plot_cmd = "plot "
	global use_lw_token

	if use_lw_token:
		linewidth = " lw LW"
	else:
		linewidth = " lw 1"

	for idx in range(0, len(col_indices) - 1):
		col_index = col_indices[idx]
		plot_cmd = plot_cmd + " \"" + datafile + "\" using 1:" 	+ str(col_index) + " with linespoint title \"" + str(columns[col_index]) + "\" " +  linewidth + ","

	col_index = col_indices[len(col_indices) - 1]
	plot_cmd = plot_cmd + " \"" + datafile + "\" using 1:" + str(col_index) + " with linespoint title \"" + str(columns[col_index]) + "\" " + linewidth + ";"
	print plot_cmd

def main(args):
	global escape_for_eps
	global use_lw_token
	prelim_file = "prelim_commands"

	datfile = args[1]
	if "--escape_for_eps" in args:
		escape_for_eps = True

	if "--use_lw_token" in args:
		use_lw_token = True
	
	cols = create_col_names(datfile)
	if "--printcols" in args:
		printcols(cols)
		sys.exit(-1)

	if "--prefile" in args:
		prelim_file = args[args.index("--prefile") + 1]

	print_prelim_cmds(prelim_file)

	if "--columns" in args:
		idx = args.index("--columns") + 1
		cols_idx = map((lambda x: int(x)), args[idx].strip().split(","))
	else:
		cols_idx = range(1, len(cols))
	
	print_plot_cmd(datfile, cols, cols_idx)

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print "Not enough arguments: Need data filename"
		sys.exit(-1)

	main(sys.argv)



