CC=gcc
CFLAGS=-Wall -march=native
N=4

setup:
	$(CC) $(CFLAGS) -c matrixUtil.c
	$(CC) $(CFLAGS) -c main_multiply.c

first_program: first_program.c
	$(CC) $(CFLAGS) -o $@ first_program.c

multiply: matrixUtil.o main_multiply.o multiply.c
	$(CC) $(CFLAGS) -o $@ matrixUtil.o main_multiply.o multiply.c

matrixUtil.o: matrixUtil.c matrixUtil.h
	$(CC) $(CFLAGS) -c matrixUtil.c

main_multiply.o: main_multiply.c
	$(CC) $(CFLAGS) -c main_multiply.c

run_first:
	./first_program

run_multiply:
	./multiply $(N) test_cases/x$(N) test_cases/y$(N) test_cases/a$(N) 0

clean:
	rm -rf first_program
