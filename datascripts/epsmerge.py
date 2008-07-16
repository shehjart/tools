#!/usr/bin/python
import pyx
import sys



def usage():
	print "Usage: epsmerge [OPTIONS] --eps-files <epsfile1> <epsfile2>...<epsfileN>"
	print "\tOptions:"
	print "\t\t--output <outputepsfile>"
	print "\t\t--rows <rows>"
	print "\t\t--columns <cols>"
	print "\t\t--scale <scale>"
	print "\t\t--xincr <xincr>"
	print "\t\t--yincr <yincr>"
	print "\t\t--rotated"
	sys.exit()

class MergedEps:
	scale = 0.50
	output = ""
	rows = 3
	columns = 2
	
	x_start = 0
	y_start = 0
	x_curr = 0
	y_curr = 0
	current_row = 0
	current_col = 0
	x_incr = 0
	y_incr = 0
	X_MAX = 10
	Y_MAX = 20

	pagelist = []
	currentcanvas = None
	pagecount = 0

	def calc_y_incr(self, yincr, rows):
		if yincr is None:
			return 7
		else:
			return yincr

	def calc_x_incr(self, xincr, cols):
		if xincr is None:
			return 9
		else:
			return xincr

	def calc_scale(self, scale, rows, columns):
		if scale is None:
			return 0.75
		else:
			return scale

	def __init__(self, output, rows, columns, xincr = None,
			yincr = None, scale = None, rotate = None):
		self.scale = self.calc_scale(scale, rows, columns)
		self.output = output
		self.x_curr = self.x_start
		self.y_curr = self.y_start
		self.currentcanvas = pyx.canvas.canvas()
		if rotate is None or rotate is False:
			self.rotated = 0
			self.rows = rows
			self.columns = columns
			self.x_incr = self.calc_x_incr(xincr, columns)
			self.y_incr = self.calc_y_incr(yincr, rows)
		else:
			self.rows = columns
			self.columns = rows
			self.rotated = 1
			self.x_incr = self.calc_y_incr(yincr, columns)
			self.y_incr = self.calc_x_incr(xincr, rows)
		
		print "MergedEps: scale:" + str(self.scale) + ", rows: " + str(self.rows) + ", columns: " + str(self.columns) + ", xincr: " + str(self.x_incr) + ", yincr: " + str(self.y_incr)

	def update_rowcols(self):
		self.current_col = self.current_col + 1
		if self.current_col == self.columns:
			self.current_row = self.current_row + 1
			self.current_col = 0

	
	def add_current_page(self):
		self.pagecount = self.pagecount + 1
		epspage = pyx.document.page(self.currentcanvas,
				"page" + str(self.pagecount), pyx.document.paperformat.A4, 
				rotated = self.rotated, margin = 0.5)
		self.pagelist.append(epspage)

	def update_pagelist(self):
		if self.current_row == self.rows:
			print "Adding page " + str(self.pagecount + 1)
			self.add_current_page()
			self.currentcanvas = pyx.canvas.canvas()
			self.current_row = 0
			self.current_col = 0


	def get_current_xy(self):
		x = self.current_col * self.x_incr
		y = self.current_row * self.y_incr

		return (x,y)

	def epsmerge(self, epsfile):
		(x, y) = self.get_current_xy()
		print "Merging " + epsfile + " at " + str(x) + "," + str(y)
		self.currentcanvas.insert(pyx.epsfile.epsfile(x, y, epsfile, scale = self.scale))

		self.update_rowcols()
		self.update_pagelist()
	

	def writefile(self):
		self.add_current_page()
		#after creating all the pages, add the list of pages to a document.
		epsdocument = pyx.document.document(self.pagelist)
		epsdocument.writePSfile(self.output)



def main(arglist):

	if "--output" in arglist:
		output = arglist[arglist.index("--output") + 1]
	else:
		print "No output file specified."
		usage()
	
	if "--rows" in arglist:
		rows = int(arglist[arglist.index("--rows") + 1])
	else:
		print "Count of rows not specified."
		usage()

	if "--columns" in arglist:
		columns = int(arglist[arglist.index("--columns") + 1])
	else:
		print "Count of columns not specified."
		usage()

	if "--eps-files" in arglist:
		epsfiles = arglist[arglist.index("--eps-files") + 1:]
	else:
		print "List of eps files not given."
		usage()

	if "--scale" in arglist:
		scale = float(arglist[arglist.index("--scale") + 1])
	else:
		scale = None
	
	if "--xincr" in arglist:
		xincr = int(arglist[arglist.index("--xincr") + 1])
	else:
		xincr = None

	if "--yincr" in arglist:
		yincr = int(arglist[arglist.index("--yincr") + 1])
	else:
		yincr = None
	
	if "--rotated" in arglist:
		rotated = True
	else:
		rotated = False
		
	epsmerger = MergedEps(output, rows, columns, xincr = xincr, 
			yincr = yincr, scale = scale, rotate = rotated)
	for filename in epsfiles:
		epsmerger.epsmerge(filename)

	epsmerger.writefile()


if __name__ == "__main__":
	if len(sys.argv) <= 2: 
		usage()

	main(sys.argv)
