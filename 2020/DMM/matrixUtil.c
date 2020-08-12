#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/types.h>
#include <smmintrin.h>
#include <xmmintrin.h>

#include "matrixUtil.h"

#if 0
int main() 
{
	double *m, *a;
	m = ( double * ) malloc( 16 * sizeof( double ));
  a = ( double * ) malloc( 16 * 4 * sizeof( double ));
	
	readMatrixFromFile( "test_cases/x4", m );


  combine( 8, m, m, m, m, a );
  printMatrix( 8, a);
	free( m );
  free( a );
	return 0;
}
#endif

void readMatrixFromFile( char *filepath, double *m )
{
	FILE *inFile;
	ssize_t nread;
	size_t len = 0;
	char *line = NULL;
	char *token;
	int i = 0;

	inFile = fopen( filepath, "r" );

	while(( nread = getline( &line, &len, inFile )) != -1 ) {
		token = strtok( line, " " );
		while( token != NULL ) {
			*( m + i++ ) = atof( token );
			token = strtok( NULL, " " );
		}
	}
  free( line );
  free( token );
	fclose( inFile );
}

int checkAnswer( int n, double *result, double *answer, int debug )
{
	int i;
	int correct = 1;

	for ( i = 0; i < n * n; i++ ) {
		if ( fabs( *( result + i ) - *( answer + i ) ) > EPSILON ) {
			printf( "multiply answer: %.14lf	correct answer: %.14lf\n", *( result + i ), *( answer + i ));
			correct = 0;
		} else if ( debug )  {
			printf( "multiply answer: %.14lf	correct answer: %.14lf\n", *( result + i ), *( answer + i ));
		}
	}
	return correct;
}
		
void readMatrixFromFile_float( char *filepath, float *m )
{
	FILE *inFile;
	ssize_t nread;
	size_t len = 0;
	char *line = NULL;
	char *token;
	int i = 0;

	inFile = fopen( filepath, "r" );

	while(( nread = getline( &line, &len, inFile )) != -1 ) {
		token = strtok( line, " " );
		while( token != NULL ) {
			*( m + i++ ) = (float)atof( token );
			token = strtok( NULL, " " );
		}
	}
  free( line );
  free( token );
	fclose( inFile );
}

int checkAnswer_float( int n, float *result, float *answer, int debug )
{
	int i;
	int correct = 1;

	for ( i = 0; i < n * n; i++ ) {
		if ( fabs( *( result + i ) - *( answer + i ) ) > EPSILON ) {
			printf( "multiply answer: %.14lf	correct answer: %.14lf\n", *( result + i ), *( answer + i ));
			correct = 0;
		} else if ( debug )  {
			printf( "multiply answer: %.14lf	correct answer: %.14lf\n", *( result + i ), *( answer + i ));
		}
	}
	return correct;
}
 		
void generateMatrix( int n, double *m )
{
	        int i;
		for ( i = 0; i < n * n; i++ ) {
			*(m + i) = rand() % 50; // mod 50 just for testing purposes
	        }

}

void addMatrix( int n, double *m1, double *m2, double *answer ) {
  int i;
  for( i = 0; i < n * n; i++ ) {
    *( answer + i ) = *( m1 + i) + *( m2 + i );
  }
}

void subtractMatrix( int n, double *m1, double *m2, double *answer ) {
  int i;
  for( i = 0; i < n * n; i++ ) {
    *( answer + i ) = *( m1 + i) - *( m2 + i );
  }
}

void split( int n, int quadrant, double *m, double *result ) {
  int start_i, start_j;

  switch( quadrant ) {
    case 1:
      start_i = 0;
      start_j = 0;
      break;
    case 3:
      start_i = n / 2;
      start_j = 0;
      break;
    case 2:
      start_i = 0;
      start_j = n / 2;
      break;
    case 4:
      start_i = n / 2;
      start_j = n / 2;
      break;
  }

  int i, j;
  for( i = 0; i < ( n / 2 ); i++ ) {
    for( j = 0; j < ( n / 2 ); j++ ) {
      *( result + ( n / 2 ) * i + j ) = *( m + ( start_i + i ) * ( n ) + ( start_j + j ) );
    }
  }
}

void combine( int n, double *a, double *b, double *c, double *d, double *result ) {
  int i, j;
  for( i = 0; i < ( n / 2 ); i++ ) {
    for( j = 0; j < ( n / 2 ); j++ ) {
      *( result + n * i + j ) = *( a + ( n / 2) * i + j );
    }
  }
  for( i = 0; i < ( n / 2 ); i++ ) {
    for( j = 0; j < ( n / 2); j++ ) {
      *( result + n * i + j + n/2 ) = *( b + ( n / 2 ) * i + j );
    }
  }
  for( i = 0; i < ( n / 2 ); i++ ) {
    for( j = 0; j < ( n / 2 ); j++ ) {
      *( result + n * ( i + n / 2) + j ) = *( c + ( n / 2 ) * i + j );
    }
  }
  for( i = 0; i < ( n / 2 ); i++ ) {
    for( j = 0; j < ( n / 2 ); j++ ) {
      *( result + n * ( i + n / 2 ) + j + n / 2 ) = *( d + ( n / 2 ) * i + j );
    }
  }
}

void printMatrix( int n, double *m ) {
  int i, j;
  for( i = 0; i < n; i++ ) {
    for( j = 0; j < n; j++ ) {
      printf( "%.0lf ", *( m + n * i + j ) );
    }
    printf( "\n" );
  }
}

void dp_double( double *a, double *b, double *c ) {
  __m128d t0, t1;

  t0 = _mm_load_pd(a);
  t1 = _mm_load_pd(b);
  t0 = _mm_dp_pd(t0, t1, 0xff);
  _mm_store_pd(c, t0);
}
