# rubash

Проект по русификации командной оболочки Bash под Linux.

Утилита rubash - это обёртка вокруг /bin/bash (GNU Bourne-Again shell).
Написана на основе SO hints:
https://stackoverflow.com/questions/19880190/interactive-input-output-using-python
после неудачных попыток скрестить python+netcat+bash.
Применимо для использования "локально". Для удалённого доступа лучше всё-таки использовать ssh.
Протестирована на Python 2.7 под Debian GNU/Linux 8.6 "Jessie" x86_64.

Аналогичные программы на Python and Shell:
1. tazhate Russian-Console, https://github.com/tazhate/Russian-Console/blob/master/.bashrc
1. Sultan wrapper, https://github.com/aeroxis/sultan/blob/master/docs/sultan-examples.rst
1. ez shell for Windows/Linux/Mac, https://github.com/jerryzhujian9/ez.py/blob/master/ez/easyshell.py
1. pseudo-terminal example by Thomas Ballinger, https://gist.github.com/thomasballinger/7979808

