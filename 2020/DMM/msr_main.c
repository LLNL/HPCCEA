#include <stdio.h>
#include <stdlib.h>

#include "msrUtil.h"

#define NUM_THREADS 1

int hello = 0;
void myfunc() {
  // do a calculation
  extern int hello;
  hello++;
}

int main( int argc, char *argv[] )
{
  // msr setup
  struct msr_batch_array read_batch, write_batch, zero_batch;
  struct msr_batch_op start_op[ NUM_READ_MSRS * NUM_THREADS ], stop_op[ NUM_READ_MSRS * NUM_THREADS ], write_op[ NUM_WRITE_MSRS * NUM_THREADS ], zero_op[ NUM_ZERO_MSRS * NUM_THREADS ];
  struct msr_deltas deltas[ NUM_THREADS ];

  // open path to kernel
  int fd = open_msr_fd();

  // setup initial batches
  write_batch.numops = NUM_WRITE_MSRS * NUM_THREADS;
  write_batch.ops = write_op;

  read_batch.numops = NUM_READ_MSRS * NUM_THREADS;
  read_batch.ops = start_op;

  zero_batch.numops = NUM_ZERO_MSRS * NUM_THREADS;
  zero_batch.ops = zero_op;

  // write off counters and zero
  write_perf_count_off( fd, NUM_THREADS, &write_batch );
  zero_counter( fd, NUM_THREADS, &zero_batch );
	
  // write on couters and read initial values
	write_perf_count_on( fd, NUM_THREADS, &write_batch );
  read_msrs( fd, NUM_THREADS, &read_batch);

  int i;
  for( i = 0; i < 100000; i++ ) {
    /********* YOUR FUNCTION HERE ************************/
    myfunc();
  }


  // write off and read final values
  write_perf_count_off( fd, NUM_THREADS, &write_batch );
  read_batch.ops = stop_op;
  read_msrs( fd, NUM_THREADS, &read_batch );

  // calculate data for each thread and print data
  get_msrdata( NUM_THREADS, start_op, stop_op, deltas );
  print_msrdelta( NUM_THREADS, deltas );

  exit( 0 );

}
