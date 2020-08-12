#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <inttypes.h>
#include <xmmintrin.h>
#include <smmintrin.h>

void naiveMultiply( int n, double *m1, double *m2, double *result )
{
	int i, j, k;

	double a0, a1;
  double row[2], col[2], dp_result[2];

  /* declare enough __m128d packed doubles for multiply
   * __m218 pd1 ....; */


  // begin multiplication loops
	for ( i = 0; i < n; i++ ) 
	{
		for ( k = 0; k < n; k+=2 ) 
		{
      /* reading ahead 1 number 
       * save values in array row and load in packed double
       * __m128d pd = _mm_load_pd( double *array_mem_addr ) */
			a0 = *( m1 + n * i + k );
			if ( k + 1 < n) { 
				a1 = *( m1 + n * i + (k+1) );
			} else {
				a1 = 0;
			}






			for ( j = 0; j < n; j++ )
			{
        /* save values in array col and load in packed double
         * __m128d pd = _mm_load_pd( double *array_mem_addr ) */
				*( result + n * i + j ) += a0 * *( m2 + n * k + j ); 
				if ( k + 1 < n ) {
					*( result + n * i + j ) += a1 * *( m2 + n * (k+1) + j );
				}



        /* perform a dot product between two packed doubles
         * __m128d answer_pd = _mm_dp_pd( __m128d operand1, __m128d operand2*, 0xff ) */ 



        /* unload dot product answer into dp_result
         * _mm_store_pd( double *answer_array_mem_addr, __m128d answer_pd ) */


        // writing answer DO NOT CHANGE
				*( result + n * i + j ) += dp_result[0]; 

			}
		}
	}
}
