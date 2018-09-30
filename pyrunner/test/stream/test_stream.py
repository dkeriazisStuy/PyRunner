from pyrunner import run_file

print('Not timing out:')
run_file('stream.py', debug=True)
print('Timing out:')
run_file('stream.py', timeout=5, debug=True)

