from pyrunner import run_file

d = run_file('exception.py', debug=True)
print('Run directory:')
print(d)

