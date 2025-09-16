import subprocess
import os
import re
import colorama
from colorama import Fore,Back,Style

colorama.init()

def run_command_with_colors(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    for line in process.stdout: # type: ignore
        colored_line = line.rstrip()
        if re.fullmatch('.*::.*',colored_line):
            color = Fore.GREEN if 'PASSED' in colored_line else Fore.RED
            pos = re.search(r'::\w*',colored_line).end() # type: ignore
            colored_line = colored_line[:pos] + color + colored_line[pos:] + Fore.RESET
            
        print(colored_line)
    process.wait()
    return process.returncode

if __name__ == '__main__':
    run_command_with_colors(f'pytest {os.path.join('tests','sync')}')
    run_command_with_colors(f'pytest {os.path.join('tests','async')}')