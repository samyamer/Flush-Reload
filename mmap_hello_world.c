#include <sys/mman.h>
#include "stdio.h"
#include "stdlib.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(void){
char* a;
int fp = open("/usr/local/bin/gpg", O_RDONLY);
 struct stat statbuf;
if (fstat (fp,&statbuf) < 0)
   {printf ("fstat error");
    return 0;
   }
printf("File size is %llu bytes \n",statbuf.st_size);

char*  file_addr = (char*) mmap(0, statbuf.st_size, PROT_READ, MAP_SHARED, fp, 0);
if(file_addr < 0){
    printf("error");
}
printf("File mapped at address: %p\n",(void*)file_addr);
printf("Printing mpih_sqr_n_basecase.....\n");
//char * sqr = file_addr + 98070;
int i = 0x98070;
while ( i<0x9831f){
    printf("%hhx %hhx %hhx %hhx\n", file_addr[i], file_addr[i+1],file_addr[i+2],file_addr[i+3]);
    i+=4;
}


// print bytes at mpih_sqr_n_basecase

return 0;
}
