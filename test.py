from parse import parse, parseErrors
from subprocess import Popen, PIPE, STDOUT
import os
import time
import threading

def runAndParse(code, md5):
	# write code to temporary file
	smvfile = open(md5+".smv", 'w')
	smvfile.write(code)
	smvfile.close()

	global output
	global f

	# this function actually runs NuSMV on the temporary file
	def target():
		global output
		global f
		f = Popen(["NuSMV", md5 + ".smv"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		output = f.stdout.read()

	# Run that target function in a new thread, and kill it when it hasn't returned after 50 seconds
	thread = threading.Thread(target=target)
	thread.start()
	thread.join(50)
	if thread.is_alive():
		f.kill()
		thread.join()
		return False, [(1, "Timeout exceeded (running took more than 50 seconds)")]

	# remove the temporary file
	os.remove(md5+".smv")

	f.poll() # get return code and call appropriate parser
	if f.returncode != 0:
		return False, parseErrors(output)
	else:
		return True, parse(output)

