import unittest
import sys
import os
from typing import List, Callable

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process, Syscall, SyscallType
from labs.lab1 import sequential_scheduler

class TestLab1(unittest.TestCase):
    def run_os(self, scheduler: Callable[[List[Process]], Process], procs: List[Process]) -> List[str]:
        output = []
        
        while len(procs) > 0:
            current: Process = scheduler(procs)
            
            # 检查进程是否还有系统调用要执行
            if current.step >= len(current.syscalls):
                # 如果进程已经执行完所有系统调用，将其移除
                procs.remove(current)
                continue
                
            call = current.syscalls[current.step]
            current.step += 1
            
            if call.syscall == SyscallType.SYS_EXIT:
                procs.remove(current)
            elif call.syscall == SyscallType.SYS_WRITE:
                output.append(call.arg)
        
        return output
    
    def reference(self, procs: List[Process]) -> List[str]:
        output = []
        for proc in procs:
            for step in proc.syscalls:
                if step.syscall == SyscallType.SYS_WRITE:
                    output.append(step.arg)
                elif step.syscall == SyscallType.SYS_EXIT:
                    break
        return output
    
    def test_lab1_implemented(self):
        self.assertTrue(callable(sequential_scheduler))

    def test_function_1(self):
        """Basic 2 processes test with single step each"""
        procs = [
            Process([Syscall(SyscallType.SYS_WRITE, 'A'), Syscall(SyscallType.SYS_EXIT)]),
            Process([Syscall(SyscallType.SYS_WRITE, 'B'), Syscall(SyscallType.SYS_EXIT)])
        ]

        self.assertEqual(
            self.run_os(sequential_scheduler, procs.copy()),
            self.reference(procs)
        )

    def test_function_2(self):
        """Multiple processes with multiple steps"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, 'A'),
                Syscall(SyscallType.SYS_WRITE, 'A'),
                Syscall(SyscallType.SYS_WRITE, 'A'),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE, 'B'),
                Syscall(SyscallType.SYS_WRITE, 'B'),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE, 'C'),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]

        self.assertEqual(
            self.run_os(sequential_scheduler, procs.copy()),
            self.reference(procs)
        )

    def test_function_3(self):
        """Single process with multiple steps"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, 'X'),
                Syscall(SyscallType.SYS_WRITE, 'Y'),
                Syscall(SyscallType.SYS_WRITE, 'Z'),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]

        self.assertEqual(
            self.run_os(sequential_scheduler, procs.copy()),
            self.reference(procs)
        )

    def test_function_5(self):
        """Stress test with many processes"""
        procs = []
        for i in range(20):
            char = chr(ord('A') + (i % 26))
            proc = Process([
                Syscall(SyscallType.SYS_WRITE, char),
                Syscall(SyscallType.SYS_WRITE, char),
                Syscall(SyscallType.SYS_EXIT)
            ])
            procs.append(proc)
        
        self.assertEqual(
            self.run_os(sequential_scheduler, procs.copy()), 
            self.reference(procs)
        )

if __name__ == '__main__':
    print("=" * 60)
    print("Lab1 Tests1")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestLab1))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All Tests PASSED")
    else:
        print("❌ Some Tests FAILED")
    print("=" * 60)
