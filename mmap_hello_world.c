#include <sys/mman.h>
#include "stdio.h"
#include "stdlib.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(void){
char* a;
int fp = open("/Users/samyamer/F23/Side-Channel/Flush-Reload_Attack/test_file.txt", O_RDONLY);
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
printf("File mapped at address: %p",(void*)file_addr);
return 0;
}
