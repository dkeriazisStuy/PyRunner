from pyrunner import run_file

d = run_file('sys.py', args=['first_arg', 'second_arg'], data=['foo.txt'], debug=True)
print('Run directory:')
print(d)

