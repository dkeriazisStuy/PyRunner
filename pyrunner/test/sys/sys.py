import subprocess
import sys

def run_cmd(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf8')

def print_cmd(cmd):
    print(run_cmd(cmd), end='')

def print_dir():
    print()
    print('-----Current Dir-----')
    print_cmd(['pwd'])
    print_cmd(['ls', '.'])
    print('---------------------')

def print_root():
    print()
    print('-----Root Dir-----')
    with open('out.txt', 'w') as f:
        result = subprocess.run(['ls', '/'], stdout=subprocess.PIPE)
        print('We live in a society')
        print(result.stdout.decode('utf8'))
        f.write(result.stdout.decode('utf8'))
    print('------------------')

if __name__ == "__main__":
    print('Args are:', sys.argv, end='')
    print_dir()
    print_root()
    print_dir()

