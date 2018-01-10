#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hint: https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
# and https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order

# MS-DOS interactive cmd.exe: https://stackoverflow.com/a/33061437/966789

import sys

def windows():
	print "Windows()"
	from subprocess import Popen, check_output, PIPE, STDOUT

	while True:
		p = Popen("cmd.exe /k ", shell = True, stdin = PIPE, stdout = PIPE, stderr = STDOUT, bufsize = 1)
		s = raw_input("> ")
		#s = s.rstrip("\\") # Чтобы не уходило в бесконечный цикл
		ss = s.strip() # когда случайно добавлены пробелы перед exit
		if ss == "exit": break
		if len(ss) == 0: continue # ничего кроме пробельных символов нет
		try:
			p.stdin.write(s+"\r\n")
		except IOError as e:
			if e.errno == errno.EPIPE:
				break

		# stdout
		while True:
			#output = ""
			try:
				#output = p.stdout.read()
				#output = check_output(s, shell="True")
				output,error = p.communicate()
				sys.stdout.write(output+"\r\n")
			except IOError as e:
				continue
			else:
				break

'''
Known bugs:
> ls /root/ (Выводит stderr не сразу)
'''

def linux():
	print "Linux()"
	import os
	import fcntl
	from subprocess import Popen, PIPE, STDOUT
	import subprocess
	import errno

	def setNonBlocking(fd):
	    """
	    Set the file description of the given file descriptor to non-blocking.
	    """
	    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
	    flags = flags | os.O_NONBLOCK
	    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

	p = Popen("/bin/bash", shell = True, stdin = PIPE, stdout = PIPE, stderr = STDOUT, bufsize = 1)
	setNonBlocking(p.stdout)
	#setNonBlocking(p.stderr)

	while True:
		s = raw_input("> ")
		s = s.rstrip("\\") # Чтобы не уходило в бесконечный цикл
		ss = s.strip() # когда случайно добавлены пробелы перед exit
		if ss == "exit": break
		if len(ss) == 0: continue # ничего кроме пробельных символов нет
		try:
			p.stdin.write(s+"\n")
		except IOError as e:
			if e.errno == errno.EPIPE:
				break

		# stdout
		while True:
			output = ""
			try:
				output = p.stdout.read()
				sys.stdout.write(output)
			except IOError as e:
				continue
			else:
				break

from sys import platform
if platform == "win32":
	windows()
elif sys.platform.startswith("linux"):
	linux()

