from pyrunner import run_file

d = run_file('infinite_loop.py', debug=True)
print('Run directory:')
print(d)

