
$ nc -l -p 30000 -e /bin/bash 
bash: line 1: $'echo\r': команда не найдена
bash: line 2: $'ls\r': команда не найдена
bash: line 3: $'quit\r': команда не найдена
^C

# netstat -apn | less -S 
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:30000           0.0.0.0:*               LISTEN      12397/nc        

$ telnet 127.0.0.1 30000
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
echo
ls
quit
Connection closed by foreign host.



