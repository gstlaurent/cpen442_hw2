// taken from http://www.hackersdelight.org/hdcodetxt/crc.c.txt
// ----------------------------- crc32c --------------------------------

/* This is derived from crc32b but does table lookup. First the table
itself is calculated, if it has not yet been set up.
Not counting the table setup (which would probably be a separate
function), when compiled to Cyclops with GCC, this function executes in
7 + 13n instructions, where n is the number of bytes in the input
message. It should be doable in 4 + 9n instructions. In any case, two
of the 13 or 9 instrucions are load byte.
   This is Figure 14-7 in the text. */

#include <stdio.h>
#include <stdlib.h>

unsigned int crc32c(unsigned char *message) {
   int i, j;
   unsigned int byte, crc, mask;
   static unsigned int table[256];

   /* Set up the table, if necessary. */

   if (table[1] == 0) {
      for (byte = 0; byte <= 255; byte++) {
         crc = byte;
         for (j = 7; j >= 0; j--) {    // Do eight times.
            mask = -(crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
         }
         table[byte] = crc;
      }
   }

   /* Through with table setup, now calculate the CRC. */

   i = 0;
   crc = 0xFFFFFFFF;
   while ((byte = message[i]) != 0) {
      crc = (crc >> 8) ^ table[(crc ^ byte) & 0xFF];
      i = i + 1;
   }
   return ~crc;
}

///////////////////////////////////////////////////////////////////////////////
// Now, my actual stuff.

#include <limits.h>

#define MAX 0x100000000
#define MY_MD5 "e52fa762878387af285e6e54398b2ce4"
#define MY_STRING "graham"
#define NTHREADS 3

typedef struct {
  unsigned long long start;
  unsigned long long end;
  int thread;
  unsigned int to_match;
  unsigned char *my_string;
} Args;




void *crc_match(void *args) {
  Args a = *((Args*) args);

  unsigned char found_string[33];
  printf("Thread %d: Searching for matches between '%llx' and '%llx'\n",
      a.thread, a.start, a.end);

  unsigned long long i;
  for (i = a.start; i < a.end; i++) {
    if (i % 0x1000000 == 0) { // 2^24
      printf("Thread %d: %llx\n", a.thread, i);
    }

    snprintf(found_string, 8, "%llx", i);
    unsigned int test_hash = crc32c(found_string);

    if (test_hash == a.to_match) {
      printf("Thread %d: Match found! ----- test string crc32('%s') == found string crc32('%s') == 0x%x\n",
          a.thread, a.my_string, found_string, a.to_match);
      return NULL;
    }
  }

  printf("Thread %d: No match found between '%llx' and '%llx'\n",
      a.thread, a.start, a.end);

  return NULL;
}

void parallel_search(void) {
  unsigned char *my_string;
  
  // Problem 3 and problem 4
  my_string = MY_STRING;  // Problem 3
  my_string = MY_MD5;     // Problem 4

  unsigned int my_hash = crc32c(my_string);
  printf("Searching for hash: 0x%x\n", my_hash);

  pthread_t threads[NTHREADS];
  Args thread_args[NTHREADS];
  unsigned long long chunksize = ULONG_MAX/NTHREADS;

  int rc, i;

  /* spawn the threads */
  for (i=0; i<NTHREADS; ++i)
    {
      Args *a = &thread_args[i];
      a->start = chunksize * i;
      a->end = a->start + chunksize;
      a->thread = i;
      a->to_match = my_hash;
      a->my_string = my_string;

      printf("spawning thread %d\n", i);
      rc = pthread_create(&threads[i], NULL, crc_match, (void *) &thread_args[i]);
    }

  /* wait for threads to finish */
  for (i=0; i<NTHREADS; ++i) {
    rc = pthread_join(threads[i], NULL);
  }
}

void sequential_search(void) {
  unsigned char *my_string;
  
  // Problem 3 and problem 4
  my_string = MY_MD5;     // Problem 4
  /*my_string = MY_STRING;  // Problem 3*/
  
  ///////////////////////////////////////////////////
  unsigned int my_hash = crc32c(my_string);
  printf("Searching for hash: 0x%x\n", my_hash);

  unsigned char found_string[9];

  unsigned long i;
  for (i=0; i<MAX; i++) {
    if (i % 1000000 == 0) {
      printf("%lu\n", i);
    }

    snprintf(found_string, 8, "%lx", i);
    unsigned int h = crc32c( found_string);

    if (h == my_hash) {
      printf("Match found!\ncrc32('%s') == crc32('%s') == 0x%x\n",
          my_string, found_string, h);
      return;
    }
  }

  puts("Error! No match found!");
}



int main(int argc, char* argv[]) {
  /*sequential_search();*/
  parallel_search();
}



/*
Problem 3
(350569284, ('14740600', '86821'))

real    1011m17.217s
user    1007m1.448s
sys     4m15.552s
*/


/*
Match found!
Problem 4
crc32('e52fa762878387af285e6e54398b2ce4') == crc32('119e668') == 0x7d6fc89f

real    0m2.129s
user    0m2.128s
sys     0m0.000s
*/
