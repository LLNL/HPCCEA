#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>
#include <xmmintrin.h>
#include <smmintrin.h>

int main() {
  double a[2], b[2], c[2];
  __m128d pd_a, pd_b, pd_c;

  // load some values into arrays
  a[0] = 0;
  a[1] = 0;
  b[0] = 0;
  b[1] = 0;

  /* load arrays into __m128d packed doubles
   * __m128d pd = _mm_load_pd( double *array_mem_addr ) */





  /* Perform operation on packed doubles
   * __m128d result = _mm_[op]_pd( __m128d operand1, __m128d operand2 ) 
   * op -> add, sub, dp */




  /* Unload packed doubles into result array
   *  _mm_store_pd( double *array_mem_addr, __m128d result ) */
  




  // printing out answer
  printf( "%lf %lf\n", c[0], c[1] );


  exit( 0 );
}
