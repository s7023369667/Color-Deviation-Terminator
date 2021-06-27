import subprocess as sp

p = sp.Popen(['python3','CheckDB.py'],stdout=sp.PIPE)
print(p.communicate())

x = sp.check_output(['python3','CheckDB.py'])
print(x)