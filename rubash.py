#!/usr/bin/python
# -*- coding: utf-8 -*-
# Hint: https://stackoverflow.com/questions/19880190/interactive-input-output-using-python

import os
import fcntl

from subprocess import Popen, PIPE
import errno

def setNonBlocking(fd):
    """
    Set the file description of the given file descriptor to non-blocking.
    """
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

p = Popen("/bin/bash", stdin = PIPE, stdout = PIPE, stderr = PIPE, bufsize = 1)
setNonBlocking(p.stdout)
setNonBlocking(p.stderr)

while True:
	s = raw_input("> ")
	if len(s.strip()) == 0: continue
	try:
		p.stdin.write(s+"\n")
	except IOError as e:
		if e.errno == errno.EPIPE:
			break
	while True:
		try:
			output = p.stdout.read()
			print output
		except IOError as e:
			continue
		else:
			break

