# CS6120 Assignment 12: Just-in-Time Compiler

> The task is to implement a trace-based speculative optimizer for Bril. You’ll implement the same concept as in a tracing JIT, but in a profile-guided AOT setting: profiling, transformation, and execution will be distinct phases. The idea is to implement the “heavy lifting” for a trace-based JIT without needing all the scaffolding that a complete JIT requires, such as on-stack replacement.
