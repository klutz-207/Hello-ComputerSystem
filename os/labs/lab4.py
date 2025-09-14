import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.myos import *
from src.process import SyscallType

def my_run():
    
    while process_count() > 0:        
        current = process_schedule()
        
        call = process_step(current)
        
        if call.syscall == SyscallType.SYS_EXIT:
            # Process exits
            process_exit(current)
        elif call.syscall == SyscallType.SYS_WRITE:
            # Write the character from syscall arg to the console
            print(call.arg, end='', flush=True)
        elif call.syscall == SyscallType.SYS_WRITE_DOUBLE:
            # Write the character from syscall arg to the console twice
            print(call.arg, end='', flush=True)
            print(call.arg, end='', flush=True)
        elif call.syscall == SyscallType.SYS_FORK:
            forked_process = current.__copy__()
            process_push(forked_process)

    print() 