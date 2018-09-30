import subprocess
import sys

def run_cmd(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf8')

def print_cmd(cmd):
    print(run_cmd(cmd), end='')

print('Args are:', sys.argv)

print('-----Current Dir-----')
print_cmd(['pwd'])
print_cmd(['ls', '.'])
print('---------------------')

with open('qux.txt', 'w') as f:
    result = subprocess.run(['ls', '/'], stdout=subprocess.PIPE)
    print('We live in a society')
    print(result.stdout.decode('utf8'))
    f.write(result.stdout.decode('utf8'))

print('-----Current Dir-----')
print_cmd(['pwd'])
print_cmd(['ls', '.'])
print('---------------------')

