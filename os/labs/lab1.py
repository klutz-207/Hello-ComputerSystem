import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process
from typing import List,Optional

def sequential_scheduler(procs: List[Process]) -> Optional[Process]:
    if not procs:
    # TODO: implement a sequential scheduler
    # Simple implementation: return the first process
        raise NotImplementedError("sequential_scheduler is not implemented yet")
    return procs[0]

    
