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

# bash: cannot set terminal process group (-1): Inappropriate ioctl for device
# bash: no job control in this shell
# https://stackoverflow.com/a/690297/966789

# re-open stdout without buffering
import gc
gc.garbage.append(sys.stdout)
gc.garbage.append(sys.stderr)
sys.stdout = os.fdopen(sys.stdout.fileno(), "w+", 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), "w+", 0)

# see also, https://stackoverflow.com/a/13256908/966789
p = Popen(["/bin/bash","--norc","--noprofile","-i"],
	shell = False,
	stdin = PIPE, stdout = PIPE, stderr = STDOUT,
	bufsize = 1,
	env={"PS1":"\\u:\\h "},
	preexec_fn=os.setsid)

# https://stackoverflow.com/a/22582602/966789
# to kill processes belonging to the same process group

proc = Process(target=Dump, args=(p.stdout.fileno(),))
proc.start()

time.sleep(0.2) # приглашение после этого выхлопа баша:

while True:
	ss = raw_input("> ")
	if ss == "exit":
		# https://stackoverflow.com/a/37776347/966789
		# you could terminate the process
		p.kill()
		proc.terminate()
		break
	if len(ss) == 0: continue # ничего кроме пробельных символов нет
	p.stdin.write(ss+"\n")
	p.stdin.flush()

	time.sleep(0.2) # чтобы выхлоп stdout не затирал промт
