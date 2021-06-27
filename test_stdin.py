import subprocess as sp

x = b"test subprocess"
p = sp.Popen(['python3','InputDB.py'],stdout=sp.PIPE, stdin=sp.PIPE)
p.stdin.write(x)
print(p.communicate())

#x = sp.check_output(['python3','CheckDB.py'])
#print(x)