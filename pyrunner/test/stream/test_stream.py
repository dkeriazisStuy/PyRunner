from pyrunner import run_file

print('Not timing out:')
d = run_file('stream.py', debug=True)
print('Run directory 1:')
print(d)

print('Timing out:')
d_fail = run_file('stream.py', timeout=5, debug=True)
print('Run directory 2:')
print(d_fail)

