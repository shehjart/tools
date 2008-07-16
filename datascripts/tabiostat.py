#!/usr/bin/python
import sys
import re



nw_speed_bits_per_sec = 1000000000


def get_nw_util(file, duration):
	global nw_speed_bits_per_sec
	tx_startbytes = None
	tx_endbytes  = None
	rx_startbytes = None
	rx_endbytes = None
	rx_bytes = 0
	tx_bytes = 0
	tx_util = 0.0
	rx_util = 0.0

	f = open(file, "r")
	
	dataline = re.compile("^RX bytes")

	for line in f:
		 rawline = line.strip()
		 if dataline.match(rawline):
			 tokens = rawline.split(":")
			 #print tokens
			 rx_bytes = long(tokens[1].split()[0])
			 tx_bytes = long(tokens[2].split()[0])
			 #print str(tx_bytes) + " " + str(rx_bytes)
			 if tx_startbytes is None:
				 tx_startbytes = tx_bytes
				 rx_startbytes = rx_bytes
			 else:
				 tx_endbytes = tx_bytes
				 rx_endbytes = rx_bytes
	
	f.close()
	datatx_bits = (tx_endbytes - tx_startbytes) * 8
	datatx_bits_per_sec = datatx_bits / duration
	tx_util = (datatx_bits_per_sec / float(nw_speed_bits_per_sec)) * 100
	
	datarx_bits = (rx_endbytes - rx_startbytes) * 8
	datarx_bits_per_sec = datarx_bits / duration
	rx_util = ( datarx_bits_per_sec / float(nw_speed_bits_per_sec)) * 100
	return (tx_util, rx_util)


def get_cpu_usage(file):
	f = open(file, "r")
	cpu_seen = 0
	dataline = re.compile("^avg-cpu")
	read_next_line = False
	linecount = 0
	prev_cpu_linecount = 0
	numline = None

	for line in f:
		linecount = linecount + 1
		rawline = line.strip()
		if dataline.match(line):
			cpu_seen = cpu_seen + 1

			if cpu_seen == 2:
				read_next_line = True
				prev_cpu_linecount = linecount

		if (read_next_line is True) and linecount == prev_cpu_linecount + 1:
			#print str(linecount) + " " + str(prev_cpu_linecount)
			numline = line.strip()
			break

	f.close()	
	return numline.split()


def get_disk_util(file):

	f = open(file, "r")

	device_seen = 0
	dataline = re.compile("^Device:")
	read_next_line = False
	linecount = 0
	prev_device_linecount = 0
	numline = None

	for line in f:
		linecount = linecount + 1
		rawline = line.strip()
		if dataline.match(line):
			device_seen = device_seen + 1

			if device_seen == 2:
				read_next_line = True
				prev_device_linecount = linecount

		if (read_next_line is True) and linecount == prev_device_linecount + 1:
			#print str(linecount) + " " + str(prev_cpu_linecount)
			numline = line.strip()
			break

	f.close()
	return numline.split()[11]



def main(iostatfile, duration):

	nw_util = get_nw_util(iostatfile, duration)
	cpu_usage = get_cpu_usage(iostatfile)
	disk_util = get_disk_util(iostatfile)

	print "Disk Utilization: " + disk_util
	print "Network TX Utilization: %.2f" % nw_util[0]
	print "Network RX Utilization: %.2f" % nw_util[1]
	print "System CPU Usage: " + cpu_usage[2]
	print "System IO Wait: " + cpu_usage[3]
	print "System Idle: " + cpu_usage[5]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "USAGE: tabiostat <iostat_datafile> <duration_secs>"
		sys.exit(-1)

	main(sys.argv[1], float(sys.argv[2]))
