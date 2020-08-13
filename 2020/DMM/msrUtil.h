#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <sys/ioctl.h>

#include "msr_safe.h"

#define PRINTED_FREQ 2.6
#define NUM_READ_MSRS 5
#define NUM_WRITE_MSRS 4
#define NUM_ZERO_MSRS 6
#define NUM_WRITE_FLOP_MEM_MSRS 5
#define NUM_READ_FLOP_MEM_MSRS 3

struct msr_deltas {
  uint64_t retired_instruct;
  uint64_t cache_access;
  uint64_t cache_miss;
  uint64_t aperf;
  uint64_t mperf;
  uint64_t mem_loads;
  double instruct_per_cycle;
  double cache_miss_per_instruct;
  double mem_loads_per_cycle;
  double freq;
  double time;
};

struct msr_flop_mem_deltas {
  uint64_t flop;
  uint64_t stores;
  uint64_t loads;
};

int open_msr_fd(); 

void read_msrs( int fd, int num_cpus, struct msr_batch_array *batch );

void read_flop_mem_msrs( int fd, int num_cpus, struct msr_batch_array *batch );

void write_perf_count_on( int fd, int num_cpus, struct msr_batch_array *batch );

void write_perf_count_off( int fd, int num_cpus, struct msr_batch_array *batch );

void write_flop_mem_count_on( int fd, int num_cpus, struct msr_batch_array *batch ); 

void write_flop_mem_count_off( int fd, int num_cpus, struct msr_batch_array *batch );

void zero_counter( int fd, int num_cpus, struct msr_batch_array *batch );

void get_msrdata( int num_cpus, struct msr_batch_op begin[], struct msr_batch_op end[], struct msr_deltas delta[]); 

void get_flop_mem_msrdata( int num_cpus, struct msr_batch_op begin[], struct msr_batch_op end[], struct msr_flop_mem_deltas delta[]);

void print_msrdelta( int num_cpus, struct msr_deltas delta[] ); 

void print_flop_mem_msrdelta( int num_cpus, struct msr_flop_mem_deltas delta[] ); 

void print_debug( int num_cpus, struct msr_batch_op start[], struct msr_batch_op stop[] ); 

void msrdelta_avg( int num_cpus, struct msr_deltas delta[], struct msr_deltas *avg ); 

void print_avg( struct msr_deltas *avg ); 
