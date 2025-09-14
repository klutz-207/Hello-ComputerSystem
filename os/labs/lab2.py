import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process
from typing import List

def priority_scheduler(procs: List[Process]) -> Process:
    # TODO: implement a priority scheduler
    if not procs:
        raise ValueError("No processes available to schedule")
    
    selected_process = max(procs, key=lambda proc: proc.priority)

    return selected_process