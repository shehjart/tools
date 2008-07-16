#!/usr/bin/python
import os
import sys
import commands


def fork_cmd(id, cmd):

	try:
		pid = os.fork()
		if pid == 0:
			print "Starting process: " + id 
			output = commands.getoutput(cmd)
			print "Finished process: %d" % id
			out = open(str(id) + ".forkcmd","w")
			out.write(output)
			out.close()
			sys.exit(1)

	except OSError,e:
		print "Command fork failed: %s" % e.strerror


def forkcmd(cmd, count, id):

	for i in range(1, count + 1):
		fork_cmd(id + str(i), cmd)

if __name__ == "__main__":
	
	if len(sys.argv) < 5:
		print "Usage: forkcmd --count <count> --command <command> --id <id>"
		sys.exit(-1)

	if "--count" not in sys.argv:
		print "Need --count argument"
		sys.exit(1)
	else:
		count = int(sys.argv[sys.argv.index("--count") + 1])

	if "--command" not in sys.argv:
		print "Need --command"
		sys.exit(1)
	else:
		cmd = sys.argv[sys.argv.index("--command") + 1]

	if "--id" in sys.argv:
		id = sys.argv[sys.argv.index("--id") + 1]

	print "Will fork %d processes of %s" % (count, cmd)

	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)

	except OSError, e:
		print "Fork failed: %s" % e.strerror
		sys.exit(1)

	os.setsid()

	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	
	except OSError, e:
		print "Second fork failed: %s" % e.strerror
		sys.exit(1)

	forkcmd(cmd, count, id)
