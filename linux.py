#!/usr/bin/python
# -*- coding: utf-8 -*-
# MIT/Expat License

import sys
import os
from subprocess import Popen, PIPE, STDOUT
import errno
import select
from multiprocessing import Process
import time

def Dump(fd):
	reads = [fd]
	while True:
		ret = select.select(reads, [], [])
		s = os.read(ret[0][0],4096)
		sys.stdout.write(s)
		sys.stdout.flush()

# https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python

import ctypes
libc = ctypes.CDLL('libc.so.6')

p = Popen(["/bin/bash","-i"], shell = False,
	stdin = PIPE, stdout = PIPE, stderr = STDOUT,
	bufsize = 1,
	env={"PS1":"\\h"},
	preexec_fn=libc.setsid)

proc = Process(target=Dump, args=(p.stdout.fileno(),))
proc.start()

time.sleep(0.2)

while True:
	try:
		ss = raw_input("> ")
		if ss == "exit":
			proc.terminate()
			break
		if len(ss) == 0: continue # ничего кроме пробельных символов нет
	except IOError as e:
		print repr(e)
		proc.terminate()
		break

	try:
		p.stdin.write(ss+"\n")
		p.stdin.flush()
	except IOError as e:
		print repr(e)
		if e.errno == errno.EPIPE:
			break

	time.sleep(0.2) # чтобы выхлоп stdout не затирал промт
