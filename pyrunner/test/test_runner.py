from pyrunner import run_file

run_file('subprocessing.py', args=['in_file.txt', 'out_file.txt'], debug=True)
run_file('infinite_loop.py', debug=True)
run_file('range.py', debug=True)
