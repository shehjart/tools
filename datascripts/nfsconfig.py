#!/usr/bin/python
"""
Script for dumping NFSv3 related configurations into a file and
for reading in such a file for setting up later, may be 
on a different system.


Shehjar Tikoo, shehjart@gelato.unsw.edu.au

"""


import os
import sys
import re
import commands


def usage():
	print "USAGE: nfsconfig <Task> <Args>"
	print "<Task> can be:"
	print "\t\t--dump\n\t\t\tWrite the NFS configuration to standard output.\n"
	print "\t\t--read\n\t\t\tRead the configuration from standard input and set it on the current system. Before using this command be sure to have kept a copy of previous settings using the --dump command, in case things go wrong.\n"
	print "Args:"
	print "\t\t--c <conf_file>\n\t\t\tSpecify the configuration file. Default is .nfsconfig\n"


class configs:
	blkdevs = []
	blkdev_line = None


	def __init__(self, conf_file):

		try:
			cf = open(conf_file,"r")

		except IOError, e:
			print "Could not open config file: " + conf_file + ":" + e.strerror
			sys.exit(-1)

		self.blkdev_line = re.compile("^blkdevs")

		for line in cf:
			if self.blkdev_line.match(line):
				self.blkdevs = line.strip().split()[1].split(",")

		cf.close()



class iosched:
	config = None

	sysfs_block_path = "/sys/block/"
	#first, for each block device, we'll read these generic params
	#may be in the future, this might be configurable by the user.
	generic_params = ['nr_requests','read_ahead_kb','scheduler']
	as_params = ['antic_expire','read_batch_expire','read_expire','write_batch_expire','write_expire']
	cfq_params = ['back_seek_max','back_seek_penalty','fifo_expire_async','fifo_expire_sync','quantum','slice_async','slice_async_rq','slice_idle','slice_sync']
	dl_params = ['fifo_batch','front_merges','read_expire','write_expire','writes_starved']
	noop_params = []
	blkdev_params = {}

	def __init__(self, conf):
		self.config = conf
		self.read_current_config()

	def process_device_param(self, name, value):
		
		newval = value
		if name == "scheduler":
			for sched in value.split():
				if "[" in sched:
					newval = sched.strip("[]")
		
		return newval
	

	def read_sched_params(self, blkdev, sched):
		
		sched_params = {}
		if sched == "anticipatory":
			params = self.as_params
		elif sched == "cfq":
			params = self.cfq_params
		elif sched == "deadline":
			params = self.dl_params
		elif sched == "noop":
			params = self.noop_params

		for param in params:

			entryname = self.sysfs_block_path + blkdev + "/queue/iosched/" + param
			try:
				entry = open(entryname, "r")
			except IOError, e:
				print "iosched: Could not open sysfs entry: " + entryname + ": " + e.strerror
				sys.exit(-1)

			value = entry.read()
			sched_params[param] = value.strip()
	
		return sched_params


	def read_current_config(self):

		for blkdev in self.config.blkdevs:
			device_params = {}
			for genparam in self.generic_params:
				try:
					entryname = self.sysfs_block_path + blkdev + "/queue/" + genparam
					entry = open(entryname, "r")
				except IOError, e:
					print "iosched: Could not open sysfs entry: " + entryname + ": " + e.strerror
					sys.exit(-1)

				value = entry.read().strip()
				device_params[genparam] = self.process_device_param(genparam, value)
				entry.close()

			sched = device_params["scheduler"]
			sched_params = self.read_sched_params(blkdev, sched)
			self.blkdev_params[blkdev] = (device_params, sched_params)

	
	def dump_config(self, output):
		for blkdev in self.blkdev_params.keys():
			line = "blkdev: " + blkdev
			(device_params, sched_params) = self.blkdev_params[blkdev]
			for param in device_params.keys():
				#this is handled later
				if not param=="scheduler":
					line = line + " " + param + ":" + device_params[param]
		
			scheduler = device_params["scheduler"]
			line = line + " scheduler:" + scheduler + "("
			for param in sched_params.keys():
				line = line + param + ":" + sched_params[param] + ","
			
			output.write(line.strip(",") + ")\n")



	def write_config(self):
		for blkdev in self.blkdev_params.keys():
			(device_params, sched_params) = self.blkdev_params[blkdev]
			for param in device_params.keys():
				try:
					entryname = self.sysfs_block_path + blkdev + "/queue/" + param
					entry = open(entryname, "w")
				except IOError, e:
					print "iosched: Could not open sysfs entry: " + entryname + ": " + e.strerror
					sys.exit(-1)

				value = device_params[param]
				entry.write(value)
				entry.close()

			for param in sched_params.keys():
				entryname = self.sysfs_block_path + blkdev + "/queue/iosched/" + param
				
				try:
					entry = open(entryname, "w")
				except IOError, e:
					print "iosched: Could not open sysfs entry: " + entryname + ": " + e.strerror
					sys.exit(-1)

				value = sched_params[param]
				entry.write(value)
				entry.close()


	def read_config(self, cline):
		blkdev_line = re.compile("^blkdev:")
		if not blkdev_line.match(cline):
			return
	
		ltoks = cline.split()
		blkdev = ltoks[1].strip()
		device_params = {}
		sched_params = {}
		params = ltoks[2:]

		sched_part = re.compile("^scheduler:")
		
		for param in params:

			if sched_part.match(param):
				temp = param.split("(")
				device_params['scheduler'] = temp[0].split(":")[1]
				p = temp[1].strip(")")
				if not ":" in p:
					sched_params = {}
					continue

				temp = p.split(",")
				for p in temp:
					pname = p.split(":")[0]
					pval = p.split(":")[1]
					sched_params[pname] = pval
			else:
				pname = param.split(":")[0].strip()
				pval = param.split(":")[1].strip()
				device_params[pname] = pval

		self.blkdev_params[blkdev] = (device_params, sched_params)


def init_config_readers(conf):

	creaders = []

	creaders.append(iosched(conf))

	return creaders


def dump_configs(creaders, output):

	for cr in creaders:
		cr.dump_config(output)


def read_configs(input, creaders):

	for line in input:
		for cr in creaders:
			cr.read_config(line)

	for cr in creaders:
		cr.write_config()

def main(arglist):

	if "--c" in arglist:
		conf_file = arglist[arglist.index("--c") + 1]
	else:
		conf_file = ".nfsconfig"

	conf = configs(conf_file)
	creaders = init_config_readers(conf)

	if "--read" in arglist:
		read_configs(sys.stdin, creaders)

	if "--dump" in arglist:
		dump_configs(creaders, sys.stdout)

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "Not enough arguments."
		usage()
		sys.exit(-1)

	main(sys.argv)
