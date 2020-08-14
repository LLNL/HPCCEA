# Dense Matrix Multiplication Optimization
## with MSRs !!!!


Setup
```bash
make
```

To make msr program
```bash
make msr_program
```

To run msr program
```bash
make run_msr
```

To make intrinsics program
```bash
make first_program
```

To run intrinsics program
```bash
make run_first
```

To make matrix multiplication
```bash
make multiply
```

To run matrix multiplication
```bash
make run_multiply N=4
```
where N is the size of the matrix, which are available in the test_cases folder
X * Y = A




Code to access MSRs are in msrUtil.c

Code in msr_safe.h is from LLNL/msr-safe
