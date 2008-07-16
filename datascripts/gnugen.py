#!/usr/bin/python
"""
A program that generates gnu plot scripts given the directives to set
on the command line. The rationale is that I want to maintain a single
file with gnuplot commands in it. I also want to use the same file
when I have to either generate a plot in eps, to x11 or to png.
Without this program, I'll be required to modify the gnuplot commands
each time I want to send the output to a different destination.


For eg. if a set command inside a plot.gnu file generates eps output.
Suppose now I need to view the plot and I dont have the eps already
generated. This is what I do:

	gnugen.py plot.gnu terminal x11 | gnuplot -persist

In the same way, the script allows me to modify the labels, tics,
ranges for a one-off use without modifying the file. See function main
for a list of commands supported at present.

The script also has a small preprocessor which replaces keys inside
the input file with value provided on the command line. This is handy
in cases where the terminal command inside the gnuplot file generates
 eps. A one-off use requires me to generate a png. Firstly, this is
the basic command:

	gnugen.py plot.gnu terminal png | gnuplot > plot.png

But its possible that label sizes or line sizes from the gnuplot file
look really bad when output is a png, unlike an eps. So instead of
actually supplying a linewidth value in the gnuplot file we place
tokens in it, for eg. LW, like below:

	"plot.dat" using ..blah.. with ....blah... lw LW;


Now to generate png with lw as 1:

	gnugen.py plot.gnu terminal png LW=1 | gnuplot > plot.png

To be prevent confusion about file format, I use a .gen extention to
denote that the file must be first processed by gnugen.py because it
has tokens in it.

The script works because a set command issued earlier can be over-ridden by
issuing it again but with different setting. The script does this by
separating the set commands and outputting them first. Then it parses
the command line for any over-rides specified by the user. These
commands are output next and in the end the plot command(s) from the
file are output to stdout.

Copyright 2007, Shehjar Tikoo under the terms of the GNU General
Public License.

"""
import sys
import re


def build_dict(arg_list):

	mytokens = {}
	for arg in arg_list:
		if arg.find("=") >= 0:
			[tok, val] = arg.split("=")
			mytokens[tok] = val
	return mytokens


def preprocessor(line, mytokens):

	if len(mytokens) == 0:
		return line

	for token in mytokens.keys():
		line = line.replace(token, mytokens[token])
	
	return line

def process_file(file):

	plot_cmd = ""
	other_cmds = ""

	setre = re.compile('^set')
	tokens = build_dict(sys.argv)
	
	try:
		for line in file.readlines():
			processed_line = preprocessor(line, tokens);
			if setre.match(processed_line):
				other_cmds = other_cmds + processed_line
				#print "Other: " + line
			else:
				plot_cmd = plot_cmd + processed_line
				#print "Plot: " + line

	except:
		sys.stderr.write(sys.argv[0] + ": Error while reading file\n")
		sys.exit(0)

	return [plot_cmd, other_cmds]


def main(file):

	plot_cmd = ""
	other_cmds = ""

	[plot_cmd, other_cmds] = process_file(file)
	print other_cmds;
		
	try:
		if "terminal" in sys.argv:
			t_idx = sys.argv.index("terminal")
			print "set terminal " + sys.argv[t_idx + 1]

		if "title" in sys.argv:
			t_idx = sys.argv.index("title")
			print "set title \"" + sys.argv[t_idx + 1] + "\""

		if "xlabel" in sys.argv:
			t_idx = sys.argv.index("xlabel")
			print "set xlabel " + sys.argv[t_idx + 1] 

		if "ylabel" in sys.argv:
			t_idx = sys.argv.index("ylabel")
			print "set ylabel " + sys.argv[t_idx + 1]

		if "key" in sys.argv:
			t_idx = sys.argv.index("key")
			print "set key " + sys.argv[t_idx + 1]

		if "xtics" in sys.argv:
			t_idx = sys.argv.index("xtics")
			print "set xtics " + sys.argv[t_idx  + 1]

		if "ytics" in sys.argv:
			t_idx = sys.argv.index("ytics")
			print "set ytics " + sys.argv[t_idx + 1]

		if "xrange" in sys.argv:
			t_idx = sys.argv.index("xrange")
			print "set xrange " + sys.argv[t_idx + 1]

		if "yrange" in sys.argv:
			t_idx = sys.argv.index("yrange")
			print "set yrange " + sys.argv[t_idx + 1]

		if "output" in sys.argv:
			t_idx = sys.argv.index("output")
			print "set output " + "\"" +  sys.argv[t_idx + 1] + "\""

		if "pointsize" in sys.argv:
			t_idx = sys.argv.index("pointsize")
			print "set pointsize " + sys.argv[t_idx + 1] 

	except:
		 sys.stderr.write(sys.argv[0] + " : Some argument/option missing for " + sys.argv[t_idx] + "\n")
		 sys.exit(0)

	

	print plot_cmd

	

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "gnugen.py: Provides overrides to the set commands already inside a gnuplot file without needing to modify the file."
		print "USAGE: gnugen.py -h\t\tPrint out this help"
		print "gnugen.py <gnuplot_file> <options>"
		print "\t<gnuplot_file> contains gnuplot commands"
		print "\t<options> Are commands and arguments for those commands. gnugen runs these commands just before the plot commands so that the the commands in the file can be over-ridden at run time."
		sys.exit(0)
	
	else:
		if sys.argv[1] == "-":
			infile = sys.stdin
		else:
			try:
				infile = open(sys.argv[1])
			except IOError, er:
				sys.stderr.write(sys.argv[0] + ": " +str(er) + "\n")
				sys.exit(0)
	
		main(infile)

