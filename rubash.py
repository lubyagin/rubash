#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hint: https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
# and https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order

# MS-DOS interactive cmd.exe: https://stackoverflow.com/a/33061437/966789

# Welcome to screen scraping world

# Если сделать алиасы в питоновском коде, то они будут работать везде - и в винде, и под линукс

import sys
import os
import fcntl
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

if sys.platform.startswith("linux"):
	p = Popen("/bin/bash", shell = True, stdin = PIPE, stdout = PIPE, stderr = STDOUT, bufsize = 1)
	proc = Process(target=Dump, args=(p.stdout.fileno(),))
	proc.start()

while True:
	if sys.platform == "win32":
		p = Popen("cmd.exe /k ", shell = True, stdin = PIPE, stdout = PIPE, stderr = STDOUT, bufsize = 1)
	s = raw_input("> ")
	s = s.rstrip("\\") # Чтобы не уходило в бесконечный цикл
	ss = s.strip() # когда случайно добавлены пробелы перед exit
	if ss == "exit":
		proc.terminate()
		break
	if len(ss) == 0: continue # ничего кроме пробельных символов нет
	try:
		if sys.platform.startswith("linux"):
			p.stdin.write(s+"\n")
		elif sys.platform == "win32":
			p.stdin.write(s+"\r\n")
		p.stdin.flush()
	except IOError as e:
		if e.errno == errno.EPIPE:
			break

	# stdout
	if sys.platform == "win32":
		while True:
			try:
				output,error = p.communicate()
				sys.stdout.write(output+"\r\n")
			except IOError as e:
				continue
			else:
				break

	time.sleep(0.2) # чтобы выхлоп stdout не затирал промт
